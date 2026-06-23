SRC_FOLDER = ..
SVC_ROOT = /opt/svc/bettywhitelist
TARBALL = /tmp/bettywhitelist.tar
TARBALLZ = $(TARBALL).gz
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

package:
	tar $(EXCLUDE) -C $(SRC_FOLDER) -cf $(TARBALL) --exclude svc/bettywhitelist.service \
	  content/ requirements.txt db/bwl.db svc 
	tar $(EXCLUDE) --append -f $(TARBALL) \
	  bettywhitelist.service
	gzip --force $(TARBALL)

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

.PHONY: init package deploy venv enable test all
