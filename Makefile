.PHONY: help install test test-smoke test-regression test-parallel clean report docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install         - Install dependencies"
	@echo "  make test           - Run all tests"
	@echo "  make test-smoke     - Run smoke tests"
	@echo "  make test-regression - Run regression tests"
	@echo "  make test-parallel  - Run tests in parallel"
	@echo "  make clean          - Clean generated files"
	@echo "  make report         - Generate and open Allure report"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run tests in Docker"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest -v --tb=short

test-smoke:
	pytest -m smoke -v --tb=short

test-regression:
	pytest -m regression -v --tb=short

test-parallel:
	pytest -n 4 -v --tb=short

clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf allure-results allure-report
	rm -rf test-results screenshots logs
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

report:
	allure serve allure-results

docker-build:
	docker-compose build

docker-run:
	docker-compose up --abort-on-container-exit

