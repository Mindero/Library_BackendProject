from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.bookPublisher import BookPublisher
from src.project.schemas.bookPublisherSchema import BookPublisherSchema


class BookPublisherRepository:
    _collection: Type[BookPublisher] = BookPublisher

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookPublisher(
            self,
            session: AsyncSession,
    ) -> list[BookPublisherSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.{BookPublisher.__tablename__};"

        bookPublisher = await session.execute(text(query))

        return [BookPublisherSchema.model_validate(obj=val) for val in bookPublisher.mappings().all()]
