from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.schemas.booksSchema import BooksSchema
from src.project.models.book import Books

from src.project.core.config import settings


class BooksRepository:
    _collection: Type[Books] = Books

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_books(
        self,
        session: AsyncSession,
    ) -> list[BooksSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.books;"

        books = await session.execute(text(query))

        return [BooksSchema.model_validate(obj=book) for book in books.mappings().all()]