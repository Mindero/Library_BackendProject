from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.bookReader import BookReader
from src.project.schemas.bookReaderSchema import BookReaderSchema


class BookReaderRepository:
    _collection: Type[BookReader] = BookReader

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookReader(
            self,
            session: AsyncSession,
    ) -> list[BookReaderSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.{BookReader.__tablename__};"

        bookReader = await session.execute(text(query))

        return [BookReaderSchema.model_validate(obj=val) for val in bookReader.mappings().all()]
