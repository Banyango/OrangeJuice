.PHONY: format lint test

format:
	uvx ruff format .

lint:
	uvx ruff check . --fix

test:
	uv run pytest tests --junitxml=results/junit.xml

help:
	@echo "Available commands:"
	@echo "  make format  - Run code formatter (uvx ruff format)"
	@echo "  make lint    - Run linter (uvx ruff check)"
	@echo "  make test    - Run tests (pytest)"