"""Composition root: wire infrastructure, services and HTTP adapters."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.api.health import router
from backend.app.config.settings import Settings
from backend.app.infrastructure.clock import MonotonicClock
from backend.app.services.health import HealthService


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings if settings is not None else Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.health_service = HealthService(
            config.app_name, config.app_version, config.app_env, MonotonicClock(),
        )
        yield

    app = FastAPI(
        title=config.app_name,
        version=config.app_version,
        description='Lab 3 runtime: only the public liveness endpoint is implemented.',
        lifespan=lifespan,
    )
    app.include_router(router)
    return app
