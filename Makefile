# Variables
PYTHON := python3
PYTEST := pytest

# Targets
.PHONY: all clean install test lint format

all: clean install test lint

clean:
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTEST) tests/

lint:
	flake8 schema_analyzer tests
	mypy schema_analyzer tests

format:
	black schema_analyzer tests
	isort schema_analyzer tests