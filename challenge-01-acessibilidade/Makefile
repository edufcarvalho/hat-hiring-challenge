.PHONY: help install run test test-verbose lint clean run-migrations

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run the FastAPI server"
	@echo "  make test          - Run tests"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make lint          - Run linter"
	@echo "  make clean         - Clean up generated files"

install:
	uv sync --all-extras

run: install
	DATABASE_URL=sqlite:///./data/challenge.db \
	ECHO_ENABLED=true                          \
	uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload


test: install
	./.venv/bin/python -m pytest src/tests/ -v

test-verbose: install
	./.venv/bin/python -m pytest src/tests/ -v --tb=long

lint: install
	./.venv/bin/ruff check src/

clean:
	rm -rf __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
