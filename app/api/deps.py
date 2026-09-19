from collections.abc import AsyncGenerator

from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.services.link import LinkService
from app.services.rate_limit import RateLimitService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_redis(request: Request) -> Redis:
    redis: Redis = request.app.state.redis
    return redis


def get_link_service(
    session: AsyncSession,
    redis: Redis,
) -> LinkService:
    return LinkService(
        session=session,
        redis=redis,
    )


def get_rate_limit_service(
    redis: Redis,
) -> RateLimitService:
    return RateLimitService(redis)
