SHELL := /bin/bash
.PHONY: check

check:
	@python -m compileall veip_sdk >/dev/null
	@python -m compileall examples >/dev/null
	@echo "OK: Python syntax checks passed"
