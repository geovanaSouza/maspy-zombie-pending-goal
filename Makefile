# VENV: virtual environment path (default: .venv)
VENV ?= .venv
# PYTHON: interpreter used by the targets (default: $(VENV)/bin/python)
PYTHON ?= $(VENV)/bin/python
# MASPY: MASPY requirement to install. Defaults to the published package.
#   Fork:  MASPY="git+https://github.com/<fork>/MASPY.git@<branch>"
#   Local: MASPY="-e ../MASPY"
MASPY ?= maspy-ml

.PHONY: setup install-maspy run-zombie run-zombie-log run-within-window run-all help

setup: $(PYTHON) ## Create the venv and install the published MASPY
	uv pip install --python $(PYTHON) --reinstall-package maspy-ml -e .

$(PYTHON):
	uv venv $(VENV) --python 3.12

install-maspy: ## Install/replace MASPY (default: published; override with MASPY=...)
	uv pip install --python $(PYTHON) --reinstall-package maspy-ml $(MASPY)

run-zombie: ## Run the zombie pending goal example
	$(PYTHON) examples/zombie_pending_goal.py

run-zombie-log: ## Run the zombie pending goal example with MASPY debug logging on
	MASPY_LOG=1 $(PYTHON) examples/zombie_pending_goal.py

run-within-window: ## Run the within-window example where Goal B proceeds
	$(PYTHON) examples/within_window_goal_b_runs.py

run-all: run-zombie run-within-window ## Run all examples sequentially

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_.-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
