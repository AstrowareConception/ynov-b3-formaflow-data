PYTHON ?= python
DATASET ?= nominal
PROFILE ?=

.PHONY: setup start stop reset-data seed smoke validate test benchmark nosql quality package clean

setup:
	@echo "[setup] Checking prerequisites and preparing local files"
	@$(PYTHON) scripts/manage.py setup

start:
	@echo "[start] Starting the project PostgreSQL service only"
	@$(PYTHON) scripts/manage.py start

stop:
	@echo "[stop] Stopping project containers without deleting volumes"
	@$(PYTHON) scripts/manage.py stop

reset-data:
	@echo "[reset-data] Rebuilding the FormaFlow schemas and nominal dataset"
	@$(PYTHON) scripts/manage.py reset-data

seed:
	@echo "[seed] Loading dataset $(DATASET)"
	@$(PYTHON) scripts/manage.py seed --dataset "$(DATASET)"

smoke:
	@echo "[smoke] Checking PostgreSQL connectivity, objects and stable results"
	@$(PYTHON) scripts/manage.py smoke

validate:
	@echo "[validate] Validating the repository contract and session schedule"
	@$(PYTHON) scripts/validate_repository.py

test:
	@echo "[test] Running repository, unit and PostgreSQL integrity tests"
	@$(PYTHON) scripts/manage.py test

benchmark:
	@echo "[benchmark] Running the bounded relational benchmark"
	@$(PYTHON) scripts/manage.py benchmark

nosql:
	@echo "[nosql] Starting and validating profile $(PROFILE)"
	@$(PYTHON) scripts/manage.py nosql --profile "$(PROFILE)"

quality:
	@echo "[quality] Validating documents, configuration and automated checks"
	@$(PYTHON) scripts/manage.py quality

package:
	@echo "[package] Building the deterministic educational archive"
	@$(PYTHON) scripts/manage.py package

clean:
	@echo "[clean] Removing only generated build and dist artifacts"
	@$(PYTHON) scripts/manage.py clean
