import secrets
import string

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import LinkNotFoundError
from app.models.link import Link
from app.repositories.link import LinkRepository
from app.services.cache import CacheService

ALPHABET = string.ascii_letters + string.digits


class LinkService:
    def __init__(
        self,
        session: AsyncSession,
        redis: Redis | None = None,
    ) -> None:
        self.repository = LinkRepository(session)
        self.session = session
        self.cache = CacheService(redis) if redis is not None else None

    async def create_link(self, original_url: str) -> Link:
        short_code = generate_short_code()

        link = await self.repository.create(
            original_url=original_url,
            short_code=short_code,
        )

        await self.session.commit()

        if self.cache is not None:
            await self.cache.set(
                key=f"link:{short_code}",
                value=original_url,
                ttl=settings.cache_ttl,
            )

        return link

    async def get_by_id(self, link_id: int) -> Link:
        link = await self.repository.get_by_id(link_id)

        if link is None:
            raise LinkNotFoundError(
                f"Link with id '{link_id}' was not found."
            )

        return link

    async def get_by_short_code(self, short_code: str) -> Link:
        link = await self.repository.get_by_short_code(short_code)

        if link is None:
            raise LinkNotFoundError(
                f"Link '{short_code}' was not found."
            )

        return link

    async def resolve_redirect(self, short_code: str) -> str:
        cache_key = f"link:{short_code}"

        if self.cache is not None:
            cached_url = await self.cache.get(cache_key)

            if cached_url is not None:
                return cached_url

        link = await self.repository.get_by_short_code(short_code)

        if link is None:
            raise LinkNotFoundError(
                f"Link '{short_code}' was not found."
            )

        if self.cache is not None:
            await self.cache.set(
                key=cache_key,
                value=link.original_url,
                ttl=settings.cache_ttl,
            )

        return link.original_url

    async def record_click(self, short_code: str) -> None:
        await self.repository.increment_clicks(short_code)
        await self.session.commit()


def generate_short_code(length: int = 7) -> str:
    return "".join(
        secrets.choice(ALPHABET)
        for _ in range(length)
    )