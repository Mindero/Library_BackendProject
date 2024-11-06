from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.bookInstance import BookInstance
from src.project.schemas.bookInstanceSchema import BookInstanceSchema


class BookInstanceRepository:
    _collection: Type[BookInstance] = BookInstance

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookInstance(
            self,
            session: AsyncSession,
    ) -> list[BookInstanceSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.{BookInstance.__tablename__};"

        bookInstance = await session.execute(text(query))

        return [BookInstanceSchema.model_validate(obj=val) for val in bookInstance.mappings().all()]
