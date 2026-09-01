"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": "0.1.0"}


@router.get("/ready")
async def readiness_check() -> dict:
    return {"status": "ready"}


@router.get("/live")
async def liveness_check() -> dict:
    return {"status": "alive"}
