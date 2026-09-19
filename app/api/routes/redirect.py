from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db_session,
    get_redis,
)
from app.core.exceptions import LinkNotFoundError
from app.services.link import LinkService

router = APIRouter(tags=["redirect"])


def get_service(
    session: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis),
) -> LinkService:
    return LinkService(
        session=session,
        redis=redis,
    )


@router.get("/{short_code}")
async def redirect_to_original(
    short_code: str,
    service: LinkService = Depends(get_service),
) -> RedirectResponse:
    try:
        original_url = await service.resolve_redirect(short_code)

        await service.record_click(short_code)

        return RedirectResponse(
            url=original_url,
            status_code=(status.HTTP_307_TEMPORARY_REDIRECT),
        )

    except LinkNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        ) from exc
