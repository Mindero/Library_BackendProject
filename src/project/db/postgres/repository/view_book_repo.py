from typing import Type

from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.models.viewBook import ViewBook
from project.schemas.views.viewBookSchema import ViewBookSchema


class ViewBookRepository:
    pass
    _collection: Type[ViewBook] = ViewBook

    async def get_all_view_books(
            self,
            session: AsyncSession,
    ) -> list[ViewBookSchema]:
        query = select(self._collection)

        view_books = await session.scalars(query)

        return [ViewBookSchema.model_validate(obj=view_book) for view_book in view_books.all()]
