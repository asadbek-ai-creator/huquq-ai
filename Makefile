# Makefile for huquqAI project
# For Windows, use: make target (with Make for Windows)
# Or run commands directly with the provided scripts

.PHONY: help install install-dev install-all test lint format clean run verify-encoding

# Default target
help:
	@echo "huquqAI - Legal Knowledge Base System"
	@echo ""
	@echo "Available targets:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install with development dependencies"
	@echo "  install-all      - Install all dependencies (dev, nlp, db)"
	@echo "  verify-encoding  - Verify UTF-8 encoding support"
	@echo "  test             - Run tests"
	@echo "  test-cov         - Run tests with coverage report"
	@echo "  lint             - Run pylint"
	@echo "  format           - Format code with black and isort"
	@echo "  type-check       - Run mypy type checking"
	@echo "  clean            - Remove cache and build files"
	@echo "  run              - Start the API server"
	@echo "  dev              - Start server in development mode"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[dev,nlp,db]"

# Encoding verification
verify-encoding:
	python scripts/verify_encoding.py

# Testing targets
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Code quality targets
lint:
	pylint src/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

# Quality check all
check: format lint type-check test

# Clean targets
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf build/ dist/ 2>/dev/null || true

# Run targets
run:
	python -m src.api.main

dev:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Init targets
init:
	mkdir -p logs data/cache data/models data/ontologies data/knowledge

# Database initialization
init-db:
	python scripts/init_db.py

# Load sample data
load-sample:
	python scripts/load_sample_data.py

# Documentation
docs:
	cd docs && sphinx-build -b html . _build
