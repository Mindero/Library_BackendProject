from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.project.core.exceptions.BookGenresExceptions import BookGenresNotFound
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.models.bookGenres import BookGenres
from src.project.schemas.bookGenresSchema import BookGenresSchema, BookGenresCreateUpdateSchema


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

    async def get_by_id(
            self,
            session: AsyncSession,
            bookGenres_id: int
    ) -> BookGenresSchema:
        query = select(self._collection).where(self._collection.id_book_genres == bookGenres_id)

        result = await session.scalar(query)

        if not result:
            raise BookGenresNotFound(_id=bookGenres_id)

        return BookGenresSchema.model_validate(obj=result)

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

        try:
            created_bookGenres = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound("book_genres")

        return BookGenresSchema.model_validate(obj=created_bookGenres)

    async def update_bookGenres(
            self,
            session: AsyncSession,
            bookGenres_id: int,
            bookGenres: BookGenresCreateUpdateSchema,
    ) -> BookGenresSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_book_genres == bookGenres_id)
            .values(bookGenres.model_dump())
            .returning(self._collection)
        )

        try:
            updated_bookGenres = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise IntegrityError("book_genres")

        if not updated_bookGenres:
            raise BookGenresNotFound(_id=bookGenres_id)

        return BookGenresSchema.model_validate(obj=updated_bookGenres)

    async def delete_bookGenres(
            self,
            session: AsyncSession,
            bookGenres_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_book_genres == bookGenres_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise BookGenresNotFound(_id=bookGenres_id)
