import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_link(
    client: AsyncClient,
) -> None:

    response = await client.post(
        "/links",
        json={
            "original_url": (
                "https://example.com"
            )
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert "short_code" in data
    assert "short_url" in data
    assert data["original_url"] == (
        "https://example.com/"
    )


@pytest.mark.asyncio
async def test_create_link_invalid_url(
    client: AsyncClient,
) -> None:

    response = await client.post(
        "/links",
        json={
            "original_url": "not-a-url"
        },
    )

    assert response.status_code == 422