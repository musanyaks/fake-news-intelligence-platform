# Deployment Guide

## Prerequisites

- Docker 24.0+
- Docker Compose 2.20+
- Kubernetes 1.28+ (for K8s deployment)
- Terraform 1.6+ (for infrastructure)
- kubectl configured

## Local Development

```bash
# Clone and setup
git clone <repo>
cd fake-news-intelligence-platform
cp .env.example .env

# Install dependencies
make dev-install

# Start services
make docker-up

# Run training
make train

# Start API
make api
```

## Docker Deployment

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Scale workers
docker-compose up -d --scale api=3
```

## Kubernetes Deployment

```bash
# Apply base manifests
kubectl apply -k deployment/kubernetes/base/

# Apply staging overlay
kubectl apply -k deployment/kubernetes/overlays/staging/

# Apply production overlay
kubectl apply -k deployment/kubernetes/overlays/production/
```

## Terraform Infrastructure

```bash
cd deployment/terraform
terraform init
terraform plan
terraform apply
```

## Helm Chart

```bash
helm install fake-news ./deployment/helm/fake-news-intelligence-platform \
  --namespace fakenews \
  --create-namespace \
  --set replicaCount=3
```

## Monitoring Setup

1. Access Grafana: http://localhost:3000 (admin/admin)
2. Import dashboards from `monitoring/grafana/dashboards/`
3. Configure Prometheus data source
4. Set up alerts in Grafana

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Kafka connection refused | Ensure Zookeeper is healthy first |
| GPU not detected | Install NVIDIA Docker runtime |
| MLflow UI not loading | Check S3/minio credentials |
| Database migrations fail | Run `make migrate` manually |
