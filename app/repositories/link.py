from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.link import Link


class LinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        original_url: str,
        short_code: str,
    ) -> Link:
        link = Link(
            original_url=original_url,
            short_code=short_code,
        )

        self.session.add(link)

        await self.session.flush()
        await self.session.refresh(link)

        return link

    async def get_by_id(
        self,
        link_id: int,
    ) -> Link | None:
        result = await self.session.execute(
            select(Link).where(
                Link.id == link_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_short_code(
        self,
        short_code: str,
    ) -> Link | None:
        result = await self.session.execute(
            select(Link).where(
                Link.short_code == short_code
            )
        )

        return result.scalar_one_or_none()

    async def increment_clicks(
        self,
        short_code: str,
    ) -> None:
        await self.session.execute(
            update(Link)
            .where(Link.short_code == short_code)
            .values(
                clicks=Link.clicks + 1
            )
        )

        await self.session.flush()