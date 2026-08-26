# Makefile to help automate tasks
PYTHON_SYSTEM ?= python3
PY := $(CURDIR)/.venv/bin/python
BENCHMARK_MIN_SCORE ?= 0.95
VERSION := $(shell sed -n 's/^__version__ = "\(.*\)"/\1/p' readability/__init__.py)
DIST_FILES := dist/readability_lxml-$(VERSION)-py3-none-any.whl \
	dist/readability_lxml-$(VERSION).tar.gz

# ###########
# Tests rule!
# ###########
.PHONY: test
test: develop
	$(PY) -m pytest -q

.PHONY: benchmark
benchmark: venv develop
	$(PY) -m readability.benchmark --min-score $(BENCHMARK_MIN_SCORE)

# #######
# INSTALL
# #######
.PHONY: all
all: setup develop

venv: .venv/bin/python

setup: venv
	$(PY) -m pip install -U pip
	$(PY) -m pip install -r requirements-dev.txt

.venv/bin/python:
	test -x .venv/bin/python || $(PYTHON_SYSTEM) -m venv .venv

.PHONY: clean
clean:
	rm -rf .venv

.PHONY: develop
develop: setup
	$(PY) -m pip install -e .


# ###########
# Development
# ###########
.PHONY: clean_all
clean_all: clean

.PHONY: lint
lint: setup
	$(PY) -m flake8 readability tests benchmarks

.PHONY: check-version
check-version:
	test "$(VERSION)" = "$$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml | head -n 1)"

.PHONY: build
build:
	$(PY) -m build

.PHONY: check-dist
check-dist: setup build
	$(PY) -m twine check $(DIST_FILES)

.PHONY: check pre-release
check pre-release: develop lint test benchmark check-version check-dist

# ###########
# Deploy
# ###########
.PHONY: dist
dist: check-dist

.PHONY: upload
upload: check-dist
	$(PY) -m twine upload $(DIST_FILES)

.PHONY: bump
bump:
	test -n "$(NEW_VERSION)"
	$(PYTHON_SYSTEM) -c 'from pathlib import Path; files = [(Path("readability/__init__.py"), "__version__ = \"$(VERSION)\"", "__version__ = \"$(NEW_VERSION)\""), (Path("pyproject.toml"), "version = \"$(VERSION)\"", "version = \"$(NEW_VERSION)\"")]; contents = [(path, path.read_text(), old, new) for path, old, new in files]; assert all(old in text for path, text, old, new in contents); [path.write_text(text.replace(old, new, 1)) for path, text, old, new in contents]'
