# System Architecture

## Overview

The Fake News Intelligence Platform is a production-grade MLOps system designed to detect misinformation in news articles and social media content. It combines traditional machine learning, deep learning transformers, and ensemble methods with comprehensive monitoring and explainability.

## High-Level Architecture

```
                    +------------------+
                    |   Data Sources   |
                    |  RSS | API | Web |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |  Kafka Stream    |
                    |  (Event Bus)     |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
    +-------------------+       +-------------------+
    |  Real-time API    |       |  Batch Pipeline   |
    |  (FastAPI)        |       |  (Airflow + Spark)|
    +--------+----------+       +--------+----------+
             |                           |
             v                           v
    +-------------------+       +-------------------+
    |  Model Serving    |       |  Feature Store    |
    |  (Transformer +   |       |  (Processed Data) |
    |   Ensemble)       |       +--------+----------+
    +--------+----------+                |
             |                           v
             v                  +-------------------+
    +-------------------+       |  Model Training   |
    |  Explainability   |       |  (MLflow Tracking)|
    |  (SHAP + Attention)|      +--------+----------+
    +--------+----------+                |
             |                           v
             v                  +-------------------+
    +-------------------+       |  Model Registry   |
    |  Monitoring       |       |  (MLflow)         |
    |  (Prometheus +    |       +-------------------+
    |   Grafana +       |
    |   Evidently)      |
    +-------------------+
```

## Component Details

### 1. Data Ingestion Layer
- **News Scraper**: Async web scraper supporting RSS feeds, REST APIs, and streaming sources
- **Kafka Producer**: Streams raw articles to Kafka for downstream processing
- **Schema Validation**: Pydantic-based validation for all incoming data

### 2. Preprocessing Layer
- **Text Cleaner**: Configurable cleaning pipeline (URLs, emails, HTML, normalization)
- **Tokenizer**: HuggingFace tokenizer wrapper with batching support
- **Normalizer**: Unicode normalization, quote/dash standardization

### 3. Feature Engineering
- **Linguistic Features**: Readability scores, lexical diversity, syntactic complexity
- **Sentiment Features**: VADER sentiment analysis
- **Metadata Features**: Source credibility, author history
- **Feature Pipeline**: sklearn-compatible pipeline with standardization

### 4. Model Layer
- **Baseline Models**: Logistic Regression, Random Forest, Gradient Boosting
- **TF-IDF Model**: SGDClassifier with TF-IDF vectorization
- **Transformer**: Fine-tuned RoBERTa for sequence classification
- **Ensemble**: Stacking/Voting ensemble combining all models
- **Calibration**: Temperature scaling and isotonic regression for probability calibration

### 5. API Layer
- **FastAPI**: Async REST API with automatic OpenAPI documentation
- **Prediction Endpoints**: Single and batch prediction with explanations
- **Health Checks**: Liveness, readiness, and health endpoints
- **Middleware**: Request logging and CORS handling

### 6. Training Pipeline
- **Orchestration**: Airflow DAGs for scheduled retraining
- **Experiment Tracking**: MLflow for parameter and metric logging
- **Hyperparameter Tuning**: Optuna for automated hyperparameter search
- **Model Registry**: Versioned model storage with staging/production promotion

### 7. Monitoring
- **Prometheus**: Metrics collection (latency, throughput, error rates)
- **Grafana**: Dashboards for system and model performance
- **Evidently**: Data drift, prediction drift, and concept drift detection

## Data Flow

1. Articles are ingested from multiple sources
2. Raw articles are validated and streamed to Kafka
3. Preprocessing cleans and normalizes text
4. Features are extracted and stored
5. Models generate predictions with confidence scores
6. Explanations are generated via attention weights or SHAP
7. Predictions and explanations are stored in the database
8. Monitoring systems track performance and detect drift

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| API Framework | FastAPI |
| ML Framework | PyTorch, Transformers, scikit-learn |
| Data Processing | Pandas, NumPy, Spark |
| Streaming | Apache Kafka |
| Orchestration | Apache Airflow |
| Experiment Tracking | MLflow |
| Database | PostgreSQL |
| Cache | Redis |
| Monitoring | Prometheus, Grafana, Evidently |
| Deployment | Docker, Kubernetes, Terraform |
| CI/CD | GitHub Actions |
