"""Model management endpoints."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/model/info")
async def model_info():
    return {
        "name": "fake-news-transformer",
        "version": "1.0.0",
        "type": "roberta-base",
        "classes": ["REAL", "FAKE"],
    }


@router.get("/model/metrics")
async def model_metrics():
    return {
        "accuracy": 0.94,
        "f1_macro": 0.93,
        "precision": 0.92,
        "recall": 0.94,
    }
