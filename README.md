# Fake News Intelligence Platform

[![Tests](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/tests.yml/badge.svg)](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/tests.yml)
[![Build](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/build.yml/badge.svg)](https://github.com/musanyaks/fake-news-intelligence-platform/actions/workflows/build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade MLOps platform for detecting misinformation in news articles and social media content. Combines transformer-based deep learning, traditional ML, and comprehensive monitoring with explainable AI.

## Features

- **Multi-Model Architecture**: RoBERTa transformers + TF-IDF + ensemble methods
- **Real-time Inference**: FastAPI-based REST API with sub-100ms latency
- **Explainable AI**: SHAP values and attention visualization
- **MLOps Pipeline**: Airflow orchestration, MLflow tracking, automated retraining
- **Stream Processing**: Kafka-based ingestion for real-time article processing
- **Big Data**: Spark jobs for large-scale preprocessing and feature engineering
- **Monitoring**: Prometheus metrics, Grafana dashboards, Evidently drift detection
- **Cloud-Native**: Kubernetes deployment with Terraform infrastructure

## Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- (Optional) Kubernetes cluster

### Installation

```bash
# Clone repository
git clone https://github.com/musanyaks/fake-news-intelligence-platform.git
cd fake-news-intelligence-platform

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Install dependencies
make dev-install

# Start infrastructure services
make docker-up

# Run database migrations
make migrate

# Seed sample data
make seed-data
```

### Training

```bash
# Run full training pipeline
make train

# Hyperparameter tuning
make tune

# Register best model
python training/register_model.py --model-path models/transformer --model-name fake-news-model
```

### API

```bash
# Development server
make api

# Production server
make api-prod
```

The API will be available at `http://localhost:8000` with interactive documentation at `/docs`.

### Example API Usage

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Scientists discover groundbreaking evidence that vaccines are effective against new virus variant..."
  }'
```

**Response:**
```json
{
  "prediction": 0,
  "label": "REAL",
  "confidence": 0.94,
  "probabilities": {
    "REAL": 0.94,
    "FAKE": 0.06
  }
}
```

## Project Structure

```
fake-news-intelligence-platform/
├── api/                    # FastAPI application
├── configs/                # YAML configurations
├── data/                   # Data directories
├── docs/                   # Documentation
├── deployment/             # Docker, K8s, Terraform, Helm
├── monitoring/             # Prometheus, Grafana, Evidently
├── notebooks/              # Jupyter notebooks
├── src/                    # Core source code
│   ├── ingestion/          # Data ingestion
│   ├── preprocessing/      # Text cleaning & normalization
│   ├── features/           # Feature engineering
│   ├── models/             # ML models
│   ├── evaluation/         # Model evaluation
│   ├── explainability/     # SHAP & attention
│   ├── pipelines/          # Training & inference pipelines
│   └── utils/              # Utilities
├── tests/                  # Test suites
├── training/               # Training scripts
└── airflow/                # Airflow DAGs
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed system architecture.

## Model Card

See [docs/model_card.md](docs/model_card.md) for model details, performance metrics, and ethical considerations.

## API Documentation

See [docs/api.md](docs/api.md) for full API reference.

## Deployment

### Docker Compose (Local)

```bash
docker-compose up -d
```

Starts: API, PostgreSQL, Redis, Kafka, MLflow, Airflow, Prometheus, Grafana, Spark

### Kubernetes

```bash
kubectl apply -k deployment/kubernetes/overlays/production/
```

### Terraform (AWS)

```bash
cd deployment/terraform
terraform init
terraform plan
terraform apply
```

## Monitoring

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MLflow**: http://localhost:5000
- **Airflow**: http://localhost:8080

## Development

```bash
# Run tests
make test

# Run linters
make lint

# Format code
make format

# Run notebooks
make notebook
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- HuggingFace Transformers library
- scikit-learn community
- FastAPI framework
