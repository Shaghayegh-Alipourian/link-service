from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import (
    LinkNotFoundError,
)
from app.models.link import Link
from app.services.link import LinkService


@pytest.mark.asyncio
async def test_get_by_id() -> None:
    session = AsyncMock()

    service = LinkService(
        session=session
    )

    link = Link(
        id=1,
        original_url="https://example.com",
        short_code="abc1234",
        clicks=0,
    )

    service.repository.get_by_id = AsyncMock(
        return_value=link
    )

    result = await service.get_by_id(1)

    assert result.id == 1
    assert result.short_code == "abc1234"


@pytest.mark.asyncio
async def test_get_by_id_not_found() -> None:
    session = AsyncMock()

    service = LinkService(
        session=session
    )

    service.repository.get_by_id = AsyncMock(
        return_value=None
    )

    with pytest.raises(
        LinkNotFoundError
    ):
        await service.get_by_id(999)


@pytest.mark.asyncio
async def test_record_click() -> None:
    session = AsyncMock()

    service = LinkService(
        session=session
    )

    service.repository.increment_clicks = (
        AsyncMock()
    )

    await service.record_click(
        "abc1234"
    )

    service.repository.increment_clicks.assert_awaited_once_with(
        "abc1234"
    )

    session.commit.assert_awaited_once()