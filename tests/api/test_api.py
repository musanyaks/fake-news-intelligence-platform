"""API endpoint tests."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_pipeline():
    """Mock the inference pipeline so tests dont need the real model."""
    mock = MagicMock()
    mock.predict.return_value = {
        "prediction": 0,
        "label": "REAL",
        "confidence": 0.95,
        "probabilities": {"REAL": 0.95, "FAKE": 0.05},
    }
    mock.predict_batch.return_value = [
        {
            "prediction": 0,
            "label": "REAL",
            "confidence": 0.95,
            "probabilities": {"REAL": 0.95, "FAKE": 0.05},
        },
        {
            "prediction": 1,
            "label": "FAKE",
            "confidence": 0.88,
            "probabilities": {"REAL": 0.12, "FAKE": 0.88},
        },
    ]
    with patch("api.routes.prediction.get_pipeline", return_value=mock):
        yield mock


def test_predict():
    response = client.post(
        "/api/v1/predict",
        json={"text": "This is a test news article with enough length."},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["label"] in ["REAL", "FAKE"]
    assert 0 <= data["confidence"] <= 1


def test_predict_batch():
    response = client.post(
        "/api/v1/predict/batch",
        json={"texts": ["Article one", "Article two"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
