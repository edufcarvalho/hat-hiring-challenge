SHELL := /bin/bash

TEST_ENV := PYTHONPATH=. DATABASE_URL=sqlite:///:memory: ECHO_ENABLED=false

ENV := DATABASE_URL=sqlite:///./data/challenge.db ECHO_ENABLED=true CACHE_TTU=60

.PHONY: help install run test test-verbose lint clean check-deps

help:
	@echo -e "\033[1;34mAvailable commands:\033[0m"
	@echo "  make install       - Install dependencies"
	@echo "  make run           - Run the FastAPI server"
	@echo "  make test          - Run tests"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make lint          - Run linter"
	@echo "  make clean         - Clean up generated files"
	@echo "  make reinstall     - Regenerate files"

install:
	uv sync --all-extras

run: install
	$(ENV) uv run uvicorn main:app --host 0.0.0.0 --port 8080 --reload

test: install
	$(TEST_ENV) uv run pytest $(TEST_FILE) -v --import-mode=importlib

test-verbose: install
	$(TEST_ENV) uv run pytest $(TEST_FILE) -v --tb=long --import-mode=importlib

lint: install
	uv run ruff check src/

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -f ./data/challenge.db ./data/challenge_test.db

reinstall: clean install
