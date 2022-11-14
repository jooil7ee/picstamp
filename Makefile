SHELL := /bin/bash

# Actions
env:
	@env python3 -m venv venv
	@source venv/bin/activate && env python3 -m pip install -U -r requirements.txt && deactivate

clean:
	@rm -rf venv
