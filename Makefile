# Makefile to help automate tasks
WD := $(shell pwd)
PY := .venv/bin/python
PIP := .venv/bin/pip
PEP8 := .venv/bin/pep8
NOSE := .venv/bin/nosetests
TWINE := twine

# ###########
# Tests rule!
# ###########
.PHONY: test
test: venv develop $(NOSE)
	$(NOSE) --with-id -s tests

$(NOSE): setup

# #######
# INSTALL
# #######
.PHONY: all
all: setup develop

venv: .venv/bin/python

setup: venv
	$(PIP) install -r requirements-dev.txt

.venv/bin/python:
	test -d .venv || which python3 && python3 -m venv .venv || virtualenv .venv

.PHONY: clean
clean:
	rm -rf .venv

develop: .venv/lib/python*/site-packages/readability-lxml.egg-link

.venv/lib/python*/site-packages/readability-lxml.egg-link:
	$(PY) -m pip install --editable .


# ###########
# Development
# ###########
.PHONY: clean_all
clean_all: clean_venv

# ###########
# Deploy
# ###########
.PHONY: dist
dist:
	$(PY) -m build
	$(TWINE) check dist/*

.PHONY: upload
upload:
	$(TWINE) upload dist/*

.PHONY: version_update
version_update:
	$(EDITOR) readability/__init__.py
