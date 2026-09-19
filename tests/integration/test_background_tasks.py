import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_background_task(
    client: AsyncClient,
) -> None:
    response = await client.post("/tasks/log")

    assert response.status_code == 200

    assert response.json() == {"status": "accepted"}
