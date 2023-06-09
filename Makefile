# ----------------------------------------------------------
# ENV VARS
# ----------------------------------------------------------
BASEDIR := $(shell pwd)
SHELL := /bin/bash

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

run: lint
	@cd src && /usr/bin/env pipenv run python main.py
