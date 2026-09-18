from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import (
    RateLimitExceededError,
)
from app.services.rate_limit import (
    RateLimitService,
)


@pytest.mark.asyncio
async def test_rate_limit_allows_request() -> None:
    redis = AsyncMock()

    redis.eval.return_value = 1

    service = RateLimitService(
        redis,
        limit=100,
        window=60,
    )

    await service.check(
        "127.0.0.1"
    )

    redis.eval.assert_awaited_once()


@pytest.mark.asyncio
async def test_rate_limit_blocks_request() -> None:
    redis = AsyncMock()

    redis.eval.return_value = 101

    service = RateLimitService(
        redis,
        limit=100,
        window=60,
    )

    with pytest.raises(
        RateLimitExceededError
    ):
        await service.check(
            "127.0.0.1"
        )