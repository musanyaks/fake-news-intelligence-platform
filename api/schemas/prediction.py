"""Pydantic schemas for predictions."""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    text: str = Field(
        ..., min_length=10, max_length=10000, description="News article text to analyze"
    )


class BatchPredictionRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=100, description="Batch of texts")


class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0=REAL, 1=FAKE")
    label: str = Field(..., description="Human-readable label")
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: Dict[str, float]
    explanation: Optional[List[Dict]] = None
