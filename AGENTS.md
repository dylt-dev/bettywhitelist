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
- Create a systemd service + install it there as a proper service on a Unix socket
- Create an nginx proxy that tunnels HTTP traffic to the host
- Add a proper FQDN in DNS
- Setup certbot to get a proper cert and accept HTTPS traffic

If all this happens inside an Incus container on a VPS host, some steps will be required to proxy HTTP/S traffic through the VPS host and into the container. It might be desirable to do cert creation + management on the host as well, as this simplifies the app dev who probably doesn't care about certbot details. It'd be good to support both options.

Eventually all this can and will be handled by a single interactive function, where the user starts with a local folder, possibly not even in github, and step by step gets led to the promised land: their app on a real server with a real domain and real HTTPS. But before that, it'll be good to have an approach that guides them every step of the way, along with manual tests to confirm each step succeeded before moving on to the next step.
