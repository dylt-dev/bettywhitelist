### calling daylight functions

daylight.sh functions are available by 'case dispatch', eg daylight.sh helloworld vs source daylight.sh && helloworld. Favor case dispatch instead of source + func call. It keeps the session clean. Sourcing the script is best for interactive use, when calling functions explicitly is convenient, esp w autocomplete


#### db/bwl.db in source control

Having live data in source control can be problematic, but it's useful to have a substantially populated bwl.db in github. In part this is to address something OpenCode did, when it decided to add a tearDown which deleted the database, which was the only example of how the database ought to look. This would not have been a problem, except it wasn't in source control, so it *was* a problem. The ./db/bwl/db file should never represent actual production data, which would live on a server in a separate path, receive backup and other TLC, etc.


#### tools/ folder for tests (or lack thereof)

Other projects have standardized on a tools/ folder for putting test scripts, one-per-task. But Python already has nice standards around where to put tests and how to write them. And while sometimes it's easy to code splunge tests in bash, in general we should keep everything Python that we can. bettywhitelist is a Python web app. Keeping it Python keeps it simple.


### tests

#### test/util.py

util.py has a Tests folder. It doesn't matter if the Tests folder contains actual tests, according to unittest naming patterns. It's still a useful place for utility functions that can be run as one-offs for maintenance. Don't consider its Tests class 'stale' just because it appears to not have any tests.

### The Ballad Of True Deployment

There are a number of steps involved in going from "works on my computer" to "Ma! Hey Ma!"
- Manually deploy the app on a host, or do a `git clone` right on the host and build it there
- Create a proper github release and install the release
- Run on a Unix socket instead of a TCP/IP port
- Create a systemd service + install it there as a proper service on a Unix socket
- Create an nginx proxy that tunnels HTTP traffic to the host
- Add a proper FQDN in DNS
- Setup certbot to get a proper cert and accept HTTPS traffic
- Install Shr to automate updates

If all this happens inside an Incus container on a VPS host, some steps will be required to proxy HTTP/S traffic through the VPS host and into the container. It might be desirable to do cert creation + management on the host as well, as this simplifies the app dev who probably doesn't care about certbot details. It'd be good to support both options.

Eventually all this can and will be handled by a single interactive function, where the user starts with a local folder, possibly not even in github, and step by step gets led to the promised land: their app on a real server with a real domain and real HTTPS. But before that, it'll be good to have an approach that guides them every step of the way, along with manual tests to confirm each step succeeded before moving on to the next step.

Rough idea of steps and confirmation

- Manually deploy on host: run the same way as on local workstation, use curl to veryify endpoints. Consider embedding a special nugget of content in any HTML that gets curled, like a single-char Unicode emoji. This makes for a good test - instead of settling for a 200 you can check that expected content was received, both in a manual-visual test and in a `curl | grep`

- Create proper gitub release and install the release: same test as above, plus maybe some [[ -f ]], [[ -d ]] etc bash tests to confirm files and folders are as expected

- Run on a unix socket instead of TCP-IP port: mod the curl test to use a unix-socket, plus a bash test to confirm socket exists, and a negative curl test to confim a TCP instance is not still up

- Systemd service - This is a big one. Same test(s) as before, possibly w a different socket location, plus systemd status + journalctl checks to establish it's really a service and not just the old instance

- Create an nginx proxy that tunnels HTTP traffic to the host - add an http curl back into the testing (hello old friend!), also successful nginx -t test and systemd checks

- Add a proper FQDN in DNS - test via dig

- Setup certbot to get a proper cert and accept HTTPS traffic - same, just change your tests to use https

- Install SHR to get updates: ???

### The Ballad of True Deployment 2.0

A phased plan for taking bettywhitelist from local dev to production.
Each phase lists concrete steps, verification, and rollback.
Items in **bold** are already built — later phases depend on earlier ones.

#### Phase 0: Host Prerequisites

- **Goal:** The target host is ready to receive the app.
- **Steps:**
  - Create a non-root user (e.g. `rayray`) with sudo for install steps
  - Install `python3`, `pip`, `venv`, `sqlite3`, `curl`, `git`
  - Open firewall port 80 (and later 443) if applicable
- **Verify:** `python3 --version && pip --version && curl --version`
- **Rollback:** n/a — standard server setup
- **Missing:** No script to automate host bootstrap; consider a `tools/bootstrap-host.sh`

#### Phase 1: Manual Deploy

- **Goal:** Confirm the app runs on the host before packaging.
- **Steps:**
  - `git clone` onto the host
  - `bash create-venv.sh` (creates venv, installs deps)
  - `bash www.sh` (starts dev server on TCP port 1313)
- **Verify:**
  - `curl http://localhost:1313/list` returns 200
  - `curl http://localhost:1313/list | grep 🌞` confirms content
- **Rollback:** `pkill -f "www 1313" && rm -rf clone`
- **Automation:** None — this is a one-shot sanity check.

#### Phase 2: Release Packaging

- **Goal:** Distribute a versioned tarball via GitHub Releases.
- **Steps:**
  - Bump version, tag commit, push
  - `make package` — creates `/tmp/bettywhitelist.tar.gz`
  - Upload tarball to the GitHub Release
  - On host: download, `make init`, extract tarball, `make venv`
- **Verify:**
  - `curl http://localhost:1313/list` (same as Phase 1)
  - `[[ -f /opt/svc/bettywhitelist/bettywhitelist.sock ]]` (file layout)
  - `[[ -d /opt/svc/bettywhitelist/venv ]]`
- **Rollback:** Remove `/opt/svc/bettywhitelist`, delete the GitHub Release
- **Automation:** `make package` exists. **Missing:** `make release` target that creates the GH release, uploads the tarball, and tags the commit. Also **missing:** a GitHub Actions workflow to do this on tag push.

#### Phase 3: Unix Socket Binding

- **Goal:** Serve on a Unix domain socket instead of a TCP port.
- **Steps:**
  - Run.sh already uses `--bind "unix:$UDS_PATH"` — **this is done**
  - `make deploy` + `make venv` places files and installs deps
  - Start the app manually: `/opt/svc/bettywhitelist/svc/run.sh`
- **Verify:**
  - `curl --unix-socket /opt/svc/bettywhitelist/bettywhitelist.sock http:/list` returns 200
  - Confirm pserve or www.sh is **not** still listening on TCP 1313
- **Rollback:** Kill the gunicorn process, delete the socket file
- **Automation:** `run.sh` and `make test` (which curls the socket) **exist.**
- **Missing:** A dedicated `make start` / `make stop` target for managing the process outside of systemd.

#### Phase 4: systemd Service

- **Goal:** Managed daemon with auto-restart on failure and at boot.
- **Steps:**
  - `svc/bettywhitelist.service` **already exists**
  - `make enable` does `systemctl enable --now bettywhitelist`
  - `make deploy` symlinks the service file and reloads systemd
- **Verify:**
  - `systemctl is-active bettywhitelist` → `active`
  - `journalctl -u bettywhitelist --no-pager -n 20` — no errors
  - Same curl test as Phase 3
- **Rollback:** `systemctl disable --now bettywhitelist`, remove symlink from `/etc/systemd/system/`
- **Automation:** `make enable` and `make deploy` **exist.**
- **Missing:** `make restart` target. Service file hardcodes `User=rayray` and paths — consider templating for multi-host use.
- **Gaps:** No log rotation configured for `/opt/svc/bettywhitelist/log/*.log`. Add a `logrotate` config.

#### Phase 5: Reverse Proxy (nginx)

- **Goal:** Accept HTTP on port 80, proxy to the Unix socket.
- **Steps:**
  - Install nginx
  - Write site config (e.g. `/etc/nginx/sites-available/bettywhitelist`):
    ```nginx
    server {
        listen 80;
        server_name _;

        location / {
            proxy_pass http://unix:/opt/svc/bettywhitelist/bettywhitelist.sock;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```
  - `nginx -t && systemctl enable --now nginx`
- **Verify:**
  - `curl http://localhost/list` (TCP, no `--unix-socket`) returns 200
  - `nginx -t` passes
  - Confirm socket is still accessible directly (Phase 3 test still works)
- **Rollback:** `rm /etc/nginx/sites-enabled/bettywhitelist`, `systemctl reload nginx`
- **Automation:** None. Consider a `make nginx` target that writes the config and reloads.
- **Missing:** Nginx config should live in the repo under `svc/nginx-site.conf` and be deployed by `make deploy`.

#### Phase 6: DNS Registration

- **Goal:** Point a real domain name at the server.
- **Steps:**
  - Acquire domain (or use a subdomain of an existing one)
  - Add A record pointing to the server's public IP
  - Optionally add AAAA record for IPv6
- **Verify:** `dig +short betty.example.com` returns the server IP
- **Rollback:** Remove the DNS record
- **Automation:** Hard to automate generically (DNS provider API varies). Consider a `tools/dns.sh` that supports a few common providers (Cloudflare, Route53) via their APIs.

#### Phase 7: TLS Termination (certbot)

- **Goal:** Serve HTTPS via LetsEncrypt, with auto-renewal.
- **Steps:**
  - `certbot --nginx -d betty.example.com`
  - Follow the interactive prompts
  - Confirm auto-renew timer is active: `systemctl list-timers | grep certbot`
- **Verify:**
  - `curl https://betty.example.com/list` returns 200
  - `curl https://betty.example.com/list | grep 🌞` content check
- **Rollback:** `certbot delete --cert-name betty.example.com`, restore nginx config
- **Automation:** A `make certbot` target would simplify this.
- **Important:** If behind an Incus container (Phase 9), certbot runs on the **host**, not in the container. Nginx on the host terminates TLS before proxying to the container's socket.

#### Phase 8: Auto-Updates (GitHub Actions Self-Hosted Runner)

- **Goal:** Automatically deploy new GitHub releases.
- **Steps:**
  - Install and configure a GitHub Actions self-hosted runner (SHR) on the host
  - Create a GitHub Actions workflow (`.github/workflows/deploy.yml`) that triggers on release and runs `make all` via the SHR
  - Or: use a simple webhook + `git pull && make all` approach
- **Verify:**
  - Create a test tag, push, watch the SHR pick it up
  - After deploy, curl the site and confirm the new version is live
- **Rollback:** `systemctl disable --now bettywhitelist`, manually restore version, re-enable
- **Automation:** SHR installation script exists in the dylt project (`sunbeam download-shr-tarball`) — can be adapted. **Missing:** the `.github/workflows/deploy.yml` workflow file.
- **Alternative:** Simpler than SHR — a cron job that checks for new GH releases via the API and runs `make all` if found. Trade-off: polling vs push, no GH token needed for public repos.

#### Phase 9: Containerization (Incus)

- **Goal:** Run bettywhitelist inside a system container for isolation, with the VPS host proxying HTTP/S.
- **Changes from bare-metal flow:**
  - Install Incus on the VPS host
  - Create a container, install bettywhitelist inside it (Phases 1-4)
  - The Unix socket lives inside the container — nginx can't reach it directly
  - **Option A (host nginx, TCP bridge):** Bind gunicorn to a TCP port *inside* the container, forward that port from host to container. Nginx on the host proxies to `localhost:<port>`. **Downside:** loses the Unix socket security model.
  - **Option B (container nginx):** Run nginx *inside* the container proxying to the container's Unix socket. Host's nginx (or just port forwarding) sends traffic to the container on port 80/443. **Downside:** two layers of nginx, more moving parts.
  - **Option C (host nginx, socket forwarding via Incus proxy device):** Incus can forward a Unix socket from the host into the container using a proxy device. This is the cleanest option but requires Incus-specific config.
- **Cert management:**
  - Run certbot on the **host** (simpler — the app dev doesn't need certbot knowledge)
  - Or run certbot inside the container (more isolated but more complex)
  - Support both, default to host-side
- **Verify:** Same curl tests as Phase 5/7, run from outside the container
- **Rollback:** `incus stop bettywhitelist && incus delete bettywhitelist`
- **Missing:** Incus profile or `incus init` script in `tools/`. A `Makefile` target like `make container` would be ideal.

#### Phase 10: Interactive Deploy Wizard (future)

- **Goal:** A single command (`make deploy-all` or `tools/deploy.sh`) that walks through all phases with prompts and verification at each step.
- **Approach:**
  - Detect current phase by running verification tests — whichever test fails (or the first one that hasn't been run) is the next phase
  - Print what the phase will do, ask for confirmation, execute
  - Run verification, report pass/fail
  - On failure: offer rollback + retry, or abort
- **Design constraints:**
  - Must work from a local folder not yet in GitHub (Phase 1 starting point)
  - Must support both bare-metal and Incus paths
  - Must support both automatic (letsencrypt) and manual (self-signed) cert paths
  - Should be idempotent — rerunning a phase that already passed is a no-op
- **Missing:** The wizard itself. This is the end goal the original Ballad describes.

### Cross-cutting concerns — missing from the plan

These affect multiple phases and aren't captured in any single step:

| Concern | Phase(s) | What's needed |
|---|---|---|
| Secrets management | 0, 2 | Env file in `svc/env` referenced by service file. Should document required vars and create a template (`svc/env.template`). |
| Log rotation | 4, 5 | Gunicorn logs accumulate in `/opt/svc/bettywhitelist/log/`. Add a `logrotate` config to `svc/`. |
| Database backup | 4+ | `bwl.db` is SQLite — hot backup via `sqlite3 .backup`. Add a cron job or systemd timer. |
| Health check endpoint | 5+ | The app should have a `/_health` endpoint returning 200. Simplifies monitoring and nginx health checks. |
| CI/CD pipeline | 2, 8 | GitHub Actions workflow to build, test, and release on tag push. Currently all manual. |
| Staging environment | all | A second Incus container or separate host for pre-production testing. |
| Zero-downtime deploys | 4, 8 | systemd `Type=exec` will kill the old process before starting the new one. For zero-downtime, switch to `Type=notify` or use a socket-activated design. |
| Monitoring / alerting | 5+ | Basic uptime check (cron + curl + email/webhook). Could grow into Prometheus metrics later. |
