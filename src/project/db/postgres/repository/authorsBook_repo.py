from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.authorsBook import AuthorsBook
from src.project.schemas.authorsBookSchema import AuthorsBookSchema


class AuthorsBookRepository:
    _collection: Type[AuthorsBook] = AuthorsBook

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_authorsBook(
            self,
            session: AsyncSession,
    ) -> list[AuthorsBookSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.authors_book;"

        authors_books = await session.execute(text(query))

        return [AuthorsBookSchema.model_validate(obj=val) for val in authors_books.mappings().all()]
