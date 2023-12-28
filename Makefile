# ----------------------------------------------------------
# ENV VARS
# ----------------------------------------------------------
BASEDIR := $(shell pwd)
SHELL := /bin/bash
PYTHON := /usr/bin/python3

# Linter
FLAKE8_CFG := $(BASEDIR)/flake8.cfg

# ----------------------------------------------------------
# ACTIONS
# ----------------------------------------------------------
# For application running and testing
env:
	@/usr/bin/env pipenv install

lint:
	@/usr/bin/env pipenv run flake8 --config $(FLAKE8_CFG) .

clean:
	@rm -f history-*.sh
