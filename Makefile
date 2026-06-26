SRC_FOLDER = .
SVC_ROOT = /opt/svc/bettywhitelist
TARBALLZ = /tmp/bettywhitelist.tar.gz
STAGING = /tmp/staging
EXCLUDE = --exclude='.git' --exclude='venv' --exclude='__pycache__' \
          --exclude='test' --exclude='tools' --exclude='*.pyc'

clean:
	rm -r $(SVC_ROOT)

init:
	mkdir -p $(SVC_ROOT)/content
	mkdir -p $(SVC_ROOT)/db
	mkdir -p $(SVC_ROOT)/log
	mkdir -p $(SVC_ROOT)/venv
	mkdir -p $(SVC_ROOT)/svc
	chown -R rayray:rayray $(SVC_ROOT)

stage:
	mkdir -p $(STAGING)
	find $(STAGING) -mindepth 1 -delete
	cp -r content/ $(STAGING)/
	cp -r db/ $(STAGING)/
	cp requirements.txt $(STAGING)/
	mkdir -p $(STAGING)/svc
	cp svc/run.sh svc/env $(STAGING)/svc/
	cp svc/bettywhitelist.service $(STAGING)/

package: stage
	tar $(EXCLUDE) -C $(STAGING) -czf $(TARBALLZ) .

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

deploy:
	tar -xzf $(TARBALLZ) -C $(SVC_ROOT)
	ln -sf $(SVC_ROOT)/bettywhitelist.service /etc/systemd/system/
	systemctl daemon-reload
	chown -R rayray:rayray $(SVC_ROOT)

venv:
	python3 -m venv $(SVC_ROOT)/venv
	$(SVC_ROOT)/venv/bin/pip install -r $(SVC_ROOT)/requirements.txt
	chown -R rayray:rayray $(SVC_ROOT)

enable:
	systemctl enable --now bettywhitelist

test:
	curl --location -v --unix-socket $(SVC_ROOT)/bettywhitelist.sock http:/index.html || { echo "test failed"; exit 1; }

all: init package deploy venv enable test

.DEFAULT_GOAL := test

.PHONY: all changelog clean deploy enable init package stage test venv
	
