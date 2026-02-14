SHELL := /bin/bash
.PHONY: check test ci

check:
@python -m compileall veip_sdk >/dev/null
@python -m compileall examples >/dev/null
@echo "OK: Python syntax checks passed"

test:
@pytest -q

ci: check test
