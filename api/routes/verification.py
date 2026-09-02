"""Main verification endpoint for consumers."""
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter

from api.schemas.prediction import VerificationRequest, VerificationResponse
from src.verification import VerificationEngine

router = APIRouter()
engine = VerificationEngine()


@router.post("/verify", response_model=VerificationResponse)
async def verify(request: VerificationRequest):
    result = engine.verify(request.query, request.type)
    return VerificationResponse(**result)
