"""API tests."""
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict():
    response = client.post(
        "/api/v1/predict",
        json={
            "text": "This is a test news article with enough length to pass validation."
        },
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
