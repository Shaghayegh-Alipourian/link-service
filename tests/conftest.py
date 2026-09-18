import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.db.session import create_redis
from app.main import app


@pytest_asyncio.fixture
async def client():
    redis = create_redis()
    await redis.ping()

    app.state.redis = redis

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    await redis.aclose()