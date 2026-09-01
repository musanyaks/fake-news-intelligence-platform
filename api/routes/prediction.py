"""Prediction API routes."""

from functools import lru_cache
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.pipelines.inference_pipeline import InferencePipeline

router = APIRouter()


class PredictRequest(BaseModel):
    text: str


class BatchPredictRequest(BaseModel):
    texts: list[str]


@lru_cache(maxsize=1)
def get_pipeline() -> InferencePipeline:
    """Lazy-load the inference pipeline on first request."""
    return InferencePipeline(
        model_path="models/transformer",
        enable_explanation=True,
    )


@router.post("/predict")
def predict(request: PredictRequest) -> dict[str, Any]:
    try:
        pipeline = get_pipeline()
        return pipeline.predict(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
def predict_batch(request: BatchPredictRequest) -> list[dict[str, Any]]:
    try:
        pipeline = get_pipeline()
        return pipeline.predict_batch(request.texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))