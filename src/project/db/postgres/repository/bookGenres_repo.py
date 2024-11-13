from typing import Type

from sqlalchemy import text, insert,update,delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.bookGenres import BookGenres
from src.project.schemas.bookGenresSchema import BookGenresSchema, BookGenresCreateUpdateSchema
from src.project.core.exceptions.BookGenresExceptions import BookGenresNotFound

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
        query = select(self._collection)

        bookGenres = await session.scalars(query)

        return [BookGenresSchema.model_validate(obj=val) for val in bookGenres.all()]

    async def create_bookGenres(
            self,
            session: AsyncSession,
            bookGenres: BookGenresCreateUpdateSchema,
    ) -> BookGenresSchema:
        query = (
            insert(self._collection)
            .values(bookGenres.model_dump())
            .returning(self._collection)
        )

        created_bookGenres = await session.scalar(query)
        await session.commit()

        return BookGenresSchema.model_validate(obj=created_bookGenres)

    async def update_bookGenres(
            self,
            session: AsyncSession,
            bookGenres_id: int,
            bookGenres: BookGenresCreateUpdateSchema,
    ) -> BookGenresSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_bookGenres == bookGenres_id)
            .values(bookGenres.model_dump())
            .returning(self._collection)
        )

        updated_bookGenres = await session.scalar(query)

        if not updated_bookGenres:
            raise BookGenresNotFound(_id=bookGenres_id)

        return BookGenresSchema.model_validate(obj=updated_bookGenres)

    async def delete_bookGenres(
            self,
            session: AsyncSession,
            bookGenres_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_bookGenres == bookGenres_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise BookGenresNotFound(_id=bookGenres_id)