from unittest.mock import AsyncMock

import pytest

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