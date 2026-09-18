from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db_session,
    get_redis,
)
from app.core.exceptions import (
    LinkNotFoundError,
    RateLimitExceededError,
)
from app.schemas.link import (
    LinkCreate,
    LinkCreated,
    LinkResponse,
)
from app.services.link import LinkService
from app.services.rate_limit import RateLimitService
from pydantic import HttpUrl

router = APIRouter(
    prefix="/links",
    tags=["links"],
)


def get_service(
    session: AsyncSession = Depends(
        get_db_session
    ),
    redis: Redis = Depends(
        get_redis
    ),
) -> LinkService:
    return LinkService(
        session=session,
        redis=redis,
    )


def get_rate_limiter(
    redis: Redis = Depends(
        get_redis
    ),
) -> RateLimitService:
    return RateLimitService(redis)


@router.post(
    "",
    response_model=LinkCreated,
    status_code=status.HTTP_201_CREATED,
)
async def create_link(
    payload: LinkCreate,
    request: Request,
    service: LinkService = Depends(
        get_service
    ),
    rate_limiter: RateLimitService = Depends(
        get_rate_limiter
    ),
) -> LinkCreated:

    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    try:
        await rate_limiter.check(client_ip)

        link = await service.create_link(
            str(payload.original_url)
        )

        return LinkCreated(
            id=link.id,
            original_url=HttpUrl(link.original_url),
            short_code=link.short_code,
            created_at=link.created_at,
            clicks=link.clicks,
            short_url=f"/{link.short_code}",
        )

    except RateLimitExceededError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        ) from exc


@router.get(
    "/{link_id}",
    response_model=LinkResponse,
)
async def get_link(
    link_id: int,
    service: LinkService = Depends(
        get_service
    ),
) -> LinkResponse:

    try:
        link = await service.get_by_id(link_id)
        return LinkResponse.model_validate(link)
    except LinkNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc