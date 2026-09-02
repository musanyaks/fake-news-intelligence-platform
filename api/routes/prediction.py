"""Prediction endpoints."""
from dotenv import load_dotenv
load_dotenv()

from typing import List

from fastapi import APIRouter, HTTPException

from api.schemas.prediction import BatchPredictionRequest, PredictionRequest, PredictionResponse
from src.pipelines.inference_pipeline import InferencePipeline

router = APIRouter()
pipeline = InferencePipeline(enable_explanation=True)


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        result = pipeline.predict(request.text)
        return PredictionResponse(
            prediction=result["prediction"],
            label=result["label"],
            confidence=result["confidence"],
            probabilities=result["probabilities"],
            explanation=result.get("explanation"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    try:
        results = pipeline.predict_batch(request.texts)
        return {"predictions": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
