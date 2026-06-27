SRC_FOLDER = .
SVC_ROOT = /opt/svc/bettywhitelist
TARBALLZ = /tmp/bettywhitelist.tar.gz
STAGING = /tmp/staging
EXCLUDE = --exclude='.git' --exclude='venv' --exclude='__pycache__' \
          --exclude='test' --exclude='tools' --exclude='*.pyc'

changelog:
	@prev=$$(git tag --sort=-creatordate | head -2 | tail -1 || true); \
	echo "## What's Changed"; \
	echo ""; \
	if [ -n "$$prev" ]; then \
	  git log --oneline --no-merges "$$prev"..HEAD \
	    | while read -r line; do echo "- $$line"; done; \
	else \
	  echo "${INITIAL_MESSAGE:-Initial release}"; \
	fi

clean:
	rm -r $(SVC_ROOT)

deploy:
	@if [ -d $(SVC_ROOT) ]; then \
		mv $(SVC_ROOT) $(SVC_ROOT).old.$$(date +%Y%m%d%H%M%S); \
	fi
	mkdir -p $(SVC_ROOT)
	cp -r /tmp/bettywhitelist.latest/extracted/* $(SVC_ROOT)/
	ln -sf $(SVC_ROOT)/bettywhitelist.service /etc/systemd/system/
	chown -R rayray:rayray $(SVC_ROOT)
	python3 -m venv $(SVC_ROOT)/venv
	$(SVC_ROOT)/venv/bin/pip install -r $(SVC_ROOT)/requirements.txt
	chown -R rayray:rayray $(SVC_ROOT)
	systemctl daemon-reload

enable:

fetch:
	dl_path=$$(/opt/bin/daylight.sh github-release-download-latest --verify --extract \
	  --extract-name extracted dylt-dev bettywhitelist) && \
	  ln -sfn "$$(dirname "$$dl_path")" /tmp/bettywhitelist.latest

init:
	mkdir -p $(SVC_ROOT)/content
	mkdir -p $(SVC_ROOT)/db
	mkdir -p $(SVC_ROOT)/log
	mkdir -p $(SVC_ROOT)/venv
	mkdir -p $(SVC_ROOT)/svc
	chown -R rayray:rayray $(SVC_ROOT)

package: stage
	tar $(EXCLUDE) -C $(STAGING) -czf $(TARBALLZ) .

prune:
	rm -rf $(SVC_ROOT).old.* /tmp/bettywhitelist.release.* /tmp/bettywhitelist.latest

run:
	systemctl enable --now bettywhitelist
	systemctl restart bettywhitelist

stage:
	mkdir -p $(STAGING)
	find $(STAGING) -mindepth 1 -delete
	cp -r content/ $(STAGING)/
	cp -r db/ $(STAGING)/
	cp requirements.txt $(STAGING)/
	mkdir -p $(STAGING)/svc
	cp svc/run.sh svc/env $(STAGING)/svc/
	cp svc/bettywhitelist.service $(STAGING)/

stage-release:
	mkdir -p /tmp/bettywhitelist.latest/extracted
	find /tmp/bettywhitelist.latest/extracted -mindepth 1 -delete
	cp -r content/ /tmp/bettywhitelist.latest/extracted/
	cp -r db/ /tmp/bettywhitelist.latest/extracted/
	cp requirements.txt /tmp/bettywhitelist.latest/extracted/
	mkdir -p /tmp/bettywhitelist.latest/extracted/svc
	cp svc/run.sh svc/env /tmp/bettywhitelist.latest/extracted/svc/
	cp svc/bettywhitelist.service /tmp/bettywhitelist.latest/extracted/


test:
	curl --location -v --unix-socket $(SVC_ROOT)/bettywhitelist.sock http:/index.html || { echo "test failed"; exit 1; }

venv:

all: init fetch deploy run test

locals-only: init stage-release deploy run test

.DEFAULT_GOAL := test

.PHONY: all changelog clean deploy fetch init locals-only package prune run stage stage-release test
	
