from unittest.mock import AsyncMock

import pytest

from app.models.link import Link
from app.services.link import LinkService


@pytest.mark.asyncio
async def test_resolve_redirect_cache_hit() -> None:
    session = AsyncMock()
    redis = AsyncMock()

    service = LinkService(session=session, redis=redis)

    service.cache.get = AsyncMock(
        return_value="https://example.com"
    )
    service.repository.get_by_short_code = AsyncMock()

    result = await service.resolve_redirect("abc1234")

    assert result == "https://example.com"

    service.repository.get_by_short_code.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_redirect_cache_miss() -> None:
    session = AsyncMock()
    redis = AsyncMock()

    service = LinkService(session=session, redis=redis)

    service.cache.get = AsyncMock(return_value=None)

    link = Link(
        id=1,
        original_url="https://example.com",
        short_code="abc1234",
        clicks=0,
    )

    service.repository.get_by_short_code = AsyncMock(
        return_value=link
    )
    service.cache.set = AsyncMock()

    result = await service.resolve_redirect("abc1234")

    assert result == "https://example.com"

    service.repository.get_by_short_code.assert_awaited_once_with(
        "abc1234"
    )

    service.cache.set.assert_awaited_once()