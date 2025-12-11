SHELL := /bin/bash
.PHONY: lint test docs run-mock-tests run-live-tests

lint:
	pylint smartsheet || true

test:
	python -m pytest tests/ -q

docs:
	make -C docs-source html || true

run-mock-tests:
	chmod +x scripts/run-mock-tests.sh
	./scripts/run-mock-tests.sh --no-clone

run-live-tests:
	chmod +x scripts/run-live-tests.sh
	./scripts/run-live-tests.sh
