"""Pydantic schemas for predictions and verification."""
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000, description="News article text to analyze")


class BatchPredictionRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=100, description="Batch of texts")


class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="0=REAL, 1=FAKE")
    label: str = Field(..., description="Human-readable label")
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: Dict[str, float]
    explanation: Optional[List[Dict]] = None


class VerificationRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=15000, description="Text, URL, or claim to verify")
    type: str = Field(default="text", pattern="^(text|url|image)$", description="Input type")


class VerificationResponse(BaseModel):
    verdict: str = Field(..., description="Final verdict")
    verdict_color: str = Field(..., description="Color for UI")
    confidence: float = Field(..., ge=0.0, le=1.0)
    truth_score: float = Field(..., ge=0.0, le=100.0)
    evidence_score: float = Field(..., ge=0.0, le=100.0)
    source_credibility: float = Field(..., ge=0.0, le=100.0)
    fact_check_matches: int = Field(default=0)
    fact_check_agreement: Optional[float] = None
    explanation: str = Field(...)
    recommendation: str = Field(...)
    claim: Dict[str, Any] = Field(...)
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    fact_checks: List[Dict[str, Any]] = Field(default_factory=list)
    web_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    model_prediction: Optional[Dict[str, Any]] = None
    share_url: Optional[str] = None
