# VENV: virtual environment path (default: .venv)
VENV ?= .venv
# PYTHON: Python interpreter used by setup (default: $(VENV)/bin/python)
PYTHON ?= $(VENV)/bin/python

.PHONY: setup run-zombie run-within-window run-all help

setup: ## Create the virtual environment and install project dependencies
	uv venv $(VENV) --python 3.12
	uv pip install --python $(PYTHON) maspy-ml

run-zombie: ## Run the zombie pending goal example
	$(PYTHON) examples/zombie_pending_goal.py

run-within-window: ## Run the within-window example where Goal B proceeds
	$(PYTHON) examples/within_window_goal_b_runs.py

run-all: run-zombie run-within-window ## Run all examples sequentially

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_.-]+:.*?## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)