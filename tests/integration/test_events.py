import pytest

from app.api.routes.events import event_stream


@pytest.mark.asyncio
async def test_event_stream() -> None:
    stream = event_stream()

    first_event = await anext(stream)

    assert first_event.startswith("data: ")
    assert "heartbeat" in first_event

    await stream.aclose()