import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


@pytest.mark.asyncio
async def test_request_id_header(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/health"
    )

    assert response.status_code == 200

    assert "X-Request-ID" in response.headers