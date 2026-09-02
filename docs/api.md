# API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.fakenews-intelligence.local
```

## Authentication

API uses Bearer token authentication (configure via `SECRET_KEY` env var).

```
Authorization: Bearer <token>
```

## Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Predict Single Article

```http
POST /api/v1/predict
Content-Type: application/json

{
  "text": "Article text content here..."
}
```

**Response:**
```json
{
  "prediction": 1,
  "label": "FAKE",
  "confidence": 0.92,
  "probabilities": {
    "REAL": 0.08,
    "FAKE": 0.92
  },
  "explanation": [
    {"token": "shocking", "score": 0.85},
    {"token": "revealed", "score": 0.72}
  ]
}
```

### Batch Prediction

```http
POST /api/v1/predict/batch
Content-Type: application/json

{
  "texts": [
    "First article text...",
    "Second article text..."
  ]
}
```

**Response:**
```json
{
  "predictions": [...],
  "count": 2
}
```

### Model Info

```http
GET /api/v1/model/info
```

### Model Metrics

```http
GET /api/v1/model/metrics
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Rate Limiting

- 100 requests/minute per API key
- Batch endpoint limited to 100 texts per request
