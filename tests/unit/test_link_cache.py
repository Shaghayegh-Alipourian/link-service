from typing import Any, cast
from unittest.mock import AsyncMock, patch

import pytest

from app.models.link import Link
from app.services.link import LinkService


@pytest.mark.asyncio
async def test_resolve_redirect_cache_hit() -> None:
    session = AsyncMock()
    redis = AsyncMock()
    service = LinkService(session=session, redis=redis)

    assert service.cache is not None
    cache = service.cache

    mock_cache_get = AsyncMock(return_value="https://example.com")
    mock_get_by_short_code = AsyncMock()

    with (
        patch.object(
            cast(Any, cache),
            "get",
            mock_cache_get,
        ),
        patch.object(
            cast(Any, service.repository),
            "get_by_short_code",
            mock_get_by_short_code,
        ),
    ):
        result = await service.resolve_redirect("abc1234")

    assert result == "https://example.com"
    mock_get_by_short_code.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolve_redirect_cache_miss() -> None:
    session = AsyncMock()
    redis = AsyncMock()
    service = LinkService(session=session, redis=redis)

    assert service.cache is not None
    cache = service.cache
    link = Link(
        id=1,
        original_url="https://example.com",
        short_code="abc1234",
        clicks=0,
    )

    mock_cache_get = AsyncMock(return_value=None)
    mock_get_by_short_code = AsyncMock(return_value=link)
    mock_cache_set = AsyncMock()

    with (
        patch.object(
            cast(Any, cache),
            "get",
            mock_cache_get,
        ),
        patch.object(
            cast(Any, service.repository),
            "get_by_short_code",
            mock_get_by_short_code,
        ),
        patch.object(
            cast(Any, cache),
            "set",
            mock_cache_set,
        ),
    ):
        result = await service.resolve_redirect("abc1234")

    assert result == "https://example.com"
    mock_get_by_short_code.assert_awaited_once_with("abc1234")
    mock_cache_set.assert_awaited_once()
