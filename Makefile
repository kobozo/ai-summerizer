# Inspired by: https://blog.mathieu-leplatre.info/tips-for-your-makefile-with-python.html

PYMODULE := ai_summerizer
TESTS := tests
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)
MYPY := $(shell command -v mypy 2> /dev/null)
PYTHON=poetry run python
PYTEST=poetry run pytest
MYPY=poetry run mypy
RUFF=poetry run ruff
COVERAGE_MIN=90

.DEFAULT_GOAL := help

.PHONY: all
all: install lint test

.PHONY: help
help:
	@echo "Please use 'make <target>', where <target> is one of"
	@echo ""
	@echo "  install     install packages and prepare environment"
	@echo "  pre-commit  run pre-commit checks on all files"
	@echo "  lint        run the code linters"
	@echo "  test        run all the tests"
	@echo "  all         install, lint, and test the project"
	@echo "  clean       remove all temporary files listed in .gitignore"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."
	@echo "Most actions are configured in 'pyproject.toml'."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) run pip install --upgrade pip setuptools
	$(POETRY) install --with dev,tests,linters
	touch $(INSTALL_STAMP)

.PHONY: lint
lint: $(INSTALL_STAMP) mypy ruff

.PHONY: mypy
mypy:
	@echo "Running Mypy..."
	$(MYPY) src/ai_summerizer

.PHONY: ruff
ruff:
	@echo "Running Ruff..."
	$(RUFF) check --fix --unsafe-fixes src/ai_summerizer tests

.PHONY: test
test: $(INSTALL_STAMP)
	$(PYTEST)

.PHONY: clean
clean:
    # Delete all files in .gitignore
	git clean -Xdf

.PHONY: pre-commit
pre-commit: $(INSTALL_STAMP)
    # Run pre-commit checks on all files
	$(POETRY) run pre-commit run --all-files
