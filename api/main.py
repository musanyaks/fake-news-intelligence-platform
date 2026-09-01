"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.middleware.logging import LoggingMiddleware
from api.routes import health, model, prediction


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
