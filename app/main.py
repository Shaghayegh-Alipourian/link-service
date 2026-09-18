from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from redis.asyncio import Redis

from app.api.routes.events import (
    router as events_router,
)
from app.api.routes.health import (
    router as health_router,
)
from app.api.routes.links import (
    router as links_router,
)
from app.api.routes.redirect import (
    router as redirect_router,
)
from app.api.routes.tasks import (
    router as tasks_router,
)
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import create_redis
from app.middleware.request_id import (
    RequestIDMiddleware,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None, None]:

    configure_logging()

    redis: Redis = create_redis()

    await redis.ping()

    app.state.redis = redis

    logger.info(
        "application_started",
        environment=settings.environment,
    )

    try:
        yield

    finally:
        logger.info(
            "application_shutdown_started"
        )

        await redis.aclose()

        logger.info(
            "application_stopped"
        )


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)


app.add_middleware(
    RequestIDMiddleware
)


app.include_router(
    health_router
)

app.include_router(
    links_router
)

app.include_router(
    redirect_router
)

app.include_router(
    events_router
)

app.include_router(
    tasks_router
)