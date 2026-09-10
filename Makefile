.PHONY: test-contracts test-infra test-unit test-integration test-benchmarks test-publication test-all status

PYTHON ?= python3

test-contracts:
	$(PYTHON) -m pytest tests/contracts -q

test-infra:
	$(PYTHON) -m pytest tests/infrastructure -q

test-unit:
	$(PYTHON) -m pytest tests/unit -q

test-integration:
	$(PYTHON) -m pytest tests/integration -q

test-benchmarks:
	@echo "Benchmarks remain empty until a target-environment baseline is recorded."

test-publication:
	$(PYTHON) -m pytest tests/publication -q

test-all: test-contracts test-infra test-unit test-integration test-benchmarks test-publication

status:
	@$(PYTHON) -c 'import yaml; from pathlib import Path; [yaml.safe_load(p.read_text()) for p in Path("tests").glob("*.yaml")]; print("Design YAML: valid")'
	@echo "Implementation phase: design and contracts"
