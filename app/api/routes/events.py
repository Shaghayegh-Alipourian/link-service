import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


async def event_stream() -> AsyncGenerator[
    str,
    None,
]:
    counter = 0

    try:
        while True:
            counter += 1

            payload = {
                "event": "heartbeat",
                "counter": counter,
            }

            yield (f"data: {json.dumps(payload)}\n\n")

            await asyncio.sleep(2)

    except asyncio.CancelledError:
        raise


@router.get("/stream")
async def stream_events() -> StreamingResponse:
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )
