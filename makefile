PYTHON := python
SRC_DIR := src
TEST_DIR := tests
COV_REPORT_DIR := coverage_report

install_project:
	@echo "Running install dependencies..."
	poetry install --no-root
	@echo "Running build project..."
	pip install -e .

test:
	@echo "Cleaning cache..."
	@python -m pytest --cache-clear
	@echo "Running tests..."
	python -m pytest --cov=src --cov-branch --cov-report=term-missing -v tests

run:
	@echo "Running application..."
	@python $(SRC_DIR)/main.py vendas_exemplo.csv --format json

run_text:
	@echo "Running application..."
	@python $(SRC_DIR)/main.py vendas_exemplo.csv --format text


run_datetime:
	@echo "Running application..."
	@python $(SRC_DIR)/main.py vendas_exemplo.csv --format json --dateStart 2023-01-01 --dateEnd 2025-01-01 