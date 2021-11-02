MAKEFLAGS += --no-print-directory

.DEFAULT_GOAL := help

PY_SOURCES := biorhythm/

.PHONY: clean fmt help install install-system lint quality run setup test typecheck uninstall

BINARY_NAME := biorhythm

export BINARY_NAME

help: ## Show available targets
	@echo "biorhythm - Available targets"
	@echo ""
	@grep -hE '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*## "} {printf "  %-15s %s\n", $$1, $$2}'

setup: ## Create .venv and install dependencies
	@./.make/setup.sh

test: ## Run tests
	@./.make/test.sh

lint: ## Run linter (ruff)
	@./.make/lint.sh

fmt: ## Format code (ruff format)
	@.venv/bin/ruff format $(PY_SOURCES) tests/

typecheck: ## Run type checker (mypy)
	@.venv/bin/mypy $(PY_SOURCES)

quality: ## Format, lint, and type-check
	@.venv/bin/ruff format $(PY_SOURCES) tests/
	@./.make/lint.sh
	@.venv/bin/mypy $(PY_SOURCES)

clean: ## Remove build artifacts and __pycache__
	@./.make/clean.sh

run: ## Run the application
	@.venv/bin/python -m biorhythm.cli $(ARGS)

install: setup ## Install entry point to ~/.local/bin
	@./.make/install.sh

install-system: setup ## Install entry point to /usr/local/bin (sudo only for copy)
	@SYSTEM=1 ./.make/install.sh

uninstall: ## Remove from ~/.local/bin and /usr/local/bin (sudo only if needed)
	@./.make/uninstall.sh
