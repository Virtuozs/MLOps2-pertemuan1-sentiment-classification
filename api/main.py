"""App factory. Run with: uvicorn api.main:app"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.core.config import get_settings
from api.routers import health, predict
from api.services.predictor import Predictor


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    settings = get_settings()
    # Loaded once at startup, so a missing or broken model fails here, not on a request.
    app.state.predictor = Predictor(
        settings.model_path, settings.model_info_path, settings.model_name
    )
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Video Games Review Sentiment API",
        description="Classifies an Amazon Video Games review as positive or negative.",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(predict.router)
    return app


app = create_app()
