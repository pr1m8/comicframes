.PHONY: help install test lint format clean build

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in development mode
	uv pip install -e ".[dev]"

test:  ## Run tests
	pytest

lint:  ## Run linting
	flake8 src/ tests/
	black --check src/ tests/

format:  ## Format code
	black src/ tests/
	isort src/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build the package
	python -m build

install-build-deps:  ## Install build dependencies
	uv pip install build hatchling

test-cli:  ## Test CLI commands
	@echo "Testing CLI commands..."
	comicframes-pdf --help
	comicframes-extract --help

example:  ## Run example script
	python examples/basic_usage.py

migrate-guide:  ## Show migration guide
	python scripts/migrate_from_old_structure.py
