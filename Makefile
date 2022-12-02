SHELL := /bin/bash
FLAKE8_CONFIG := ./flake8.cfg

# Actions
env:
	@env python3 -m venv venv
	@source venv/bin/activate && env python3 -m pip install -U -r requirements.txt && deactivate

lint:
	@flake8 --config $(FLAKE8_CONFIG) .

clean:
	@rm -rf venv
