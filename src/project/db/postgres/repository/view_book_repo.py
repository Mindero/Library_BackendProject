from typing import Type

from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from project.core.config import settings
from project.db.postgres.database import metadata
from project.schemas.views.viewBookSchema import ViewBookSchema


class ViewBookRepository:

    async def get_all_view_books(
            self,
            session: AsyncSession,
    ) -> list[ViewBookSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.view_book;"

        view_books = await session.execute(text(query))

        return [ViewBookSchema.model_validate(obj=view_book) for view_book in view_books.all()]

    async def get_view_books_by_name(
            self,
            session: AsyncSession,
            name: str,
    ) -> list[ViewBookSchema]:
        print(f"name = {name}")
        # print(metadata.schema[settings.POSTGRES_SCHEMA])
        # query = f"select * from {settings.POSTGRES_SCHEMA}.view_book where book_name = {name}"
        # view_books = await session.execute(text(query))
        VIEW = metadata.tables[f"{settings.POSTGRES_SCHEMA}.view_book"]
        query = select(VIEW).where(VIEW.c.book_name == name)
        view_books = await session.execute(query)
        return [ViewBookSchema.model_validate(obj=view_book) for view_book in view_books.all()]