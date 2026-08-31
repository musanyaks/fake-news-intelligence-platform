.PHONY: help install dev-install test lint format clean docker-build docker-up docker-down train api docs

PYTHON := python3
PIP := pip3
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy

help:
	@echo "Fake News Intelligence Platform - Available Commands"
	@echo "----------------------------------------------------"
	@echo "install       - Install production dependencies"
	@echo "dev-install   - Install development dependencies"
	@echo "test          - Run all tests"
	@echo "test-unit     - Run unit tests"
	@echo "test-integration - Run integration tests"
	@echo "lint          - Run linters"
	@echo "format        - Format code with black and isort"
	@echo "clean         - Clean build artifacts"
	@echo "docker-build  - Build Docker images"
	@echo "docker-up     - Start Docker services"
	@echo "docker-down   - Stop Docker services"
	@echo "train         - Run training pipeline"
	@echo "api           - Start API server"
	@echo "docs          - Build documentation"

install:
	$(PIP) install -e .

dev-install:
	$(PIP) install -e ".[dev]"
	$(PIP) install -r requirements-dev.txt

test:
	$(PYTEST) tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit:
	$(PYTEST) tests/unit/ -v

test-integration:
	$(PYTEST) tests/integration/ -v

test-api:
	$(PYTEST) tests/api/ -v

test-model:
	$(PYTEST) tests/model/ -v

lint:
	$(FLAKE8) src/ api/ training/ tests/
	$(MYPY) src/ api/ training/

format:
	$(BLACK) src/ api/ training/ tests/
	$(ISORT) src/ api/ training/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

train:
	$(PYTHON) training/train.py --config configs/config.yaml

tune:
	$(PYTHON) training/hyperparameter_tuning.py --config configs/config.yaml

api:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

api-prod:
	gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

spark-preprocess:
	spark-submit spark/jobs/preprocessing.py

spark-features:
	spark-submit spark/jobs/feature_engineering.py

airflow-init:
	airflow db init
	airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

airflow-webserver:
	airflow webserver --port 8080

airflow-scheduler:
	airflow scheduler

docs:
	cd docs && make html

notebook:
	jupyter notebook notebooks/

seed-data:
	$(PYTHON) -c "from src.utils.database import seed_database; seed_database()"

migrate:
	$(PYTHON) -c "from src.utils.database import run_migrations; run_migrations()"
