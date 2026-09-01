"""Model management endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/model/info")
async def model_info() -> dict:
    return {
        "name": "fake-news-transformer",
        "version": "1.0.0",
        "type": "roberta-base",
        "classes": ["REAL", "FAKE"],
    }


@router.get("/model/metrics")
async def model_metrics() -> dict:
    return {
        "accuracy": 0.94,
        "f1_macro": 0.93,
        "precision": 0.92,
        "recall": 0.94,
    }
