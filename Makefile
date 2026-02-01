.PHONY: help check lint test format clean install-dev ruff black mypy

help:
	@echo "Available targets:"
	@echo "  install-dev  Install with dev dependencies"
	@echo "  check        Run lint + test"
	@echo "  lint         Run ruff, black --check, mypy"
	@echo "  test         Run pytest"
	@echo "  format       Format with black and ruff"
	@echo "  clean        Remove build artifacts"

install-dev:
	pip install -e ".[dev]"

check: lint test

lint: ruff black mypy

ruff:
	ruff check mdcrawler tests

black:
	black --check mdcrawler tests

mypy:
	mypy mdcrawler

test:
	pytest tests -v

format:
	black mdcrawler tests
	ruff check --fix mdcrawler tests

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/ htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
