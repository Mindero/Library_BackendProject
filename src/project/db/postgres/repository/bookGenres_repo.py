from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.bookGenres import BookGenres
from src.project.schemas.bookGenresSchema import BookGenresSchema


class BookGenresRepository:
    _collection: Type[BookGenres] = BookGenres

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookGenres(
            self,
            session: AsyncSession,
    ) -> list[BookGenresSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.{BookGenres.__tablename__};"

        bookGenres = await session.execute(text(query))

        return [BookGenresSchema.model_validate(obj=val) for val in bookGenres.mappings().all()]
