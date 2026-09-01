"""Prediction API routes."""

from functools import lru_cache
from typing import Any

from fastapi import APIRouter, HTTPException

from src.pipelines.inference_pipeline import InferencePipeline

router = APIRouter()


@lru_cache(maxsize=1)
def get_pipeline() -> InferencePipeline:
    """Lazy-load the inference pipeline."""
    return InferencePipeline(
        model_path="models/transformer",
        enable_explanation=True,
    )


@router.post("/predict")
def predict(text: str) -> dict[str, Any]:
    try:
        pipeline = get_pipeline()
        result = pipeline.predict(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
def predict_batch(texts: list[str]) -> list[dict[str, Any]]:
    try:
        pipeline = get_pipeline()
        return pipeline.predict_batch(texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
