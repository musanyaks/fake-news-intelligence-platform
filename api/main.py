"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()  # Load .env file automatically
from fastapi.middleware.cors import CORSMiddleware

from api.middleware.logging import LoggingMiddleware
from api.routes import health, model, prediction, verification


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.utils.logger import setup_logging
    setup_logging()
    yield


app = FastAPI(
    title="Fake News Intelligence API",
    description="Production API for fake news detection",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(prediction.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(model.router, prefix="/api/v1", tags=["Model Management"])
app.include_router(verification.router, prefix="/api/v1", tags=["Verification"])


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)