from typing import Type

from sqlalchemy import text, select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.exceptions.BookExceptions import BookNotFound
from src.project.models.book import Books
from src.project.schemas.bookSchema import BookSchema, BookCreateUpdateSchema


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
    ) -> list[BookSchema]:
        query = select(self._collection)

        books = await session.scalars(query)

        return [BookSchema.model_validate(obj=book) for book in books.all()]

    async def get_by_id(
            self,
            session: AsyncSession,
            book_id: int
    ) -> BookSchema:
        query = select(self._collection).where(self._collection.id_book == book_id)

        result = await session.scalar(query)

        if not result:
            raise BookNotFound(_id=book_id)

        return BookSchema.model_validate(obj=result)

    async def create_book(
            self,
            session: AsyncSession,
            book: BookCreateUpdateSchema,
    ) -> BookSchema:
        query = (
            insert(self._collection)
            .values(book.model_dump())
            .returning(self._collection)
        )

        created_book = await session.scalar(query)
        await session.commit()

        return BookSchema.model_validate(obj=created_book)

    async def update_book(
            self,
            session: AsyncSession,
            book_id: int,
            book: BookCreateUpdateSchema,
    ) -> BookSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_book == book_id)
            .values(book.model_dump())
            .returning(self._collection)
        )

        updated_author = await session.scalar(query)

        if not updated_author:
            raise BookNotFound(_id=book_id)

        return BookSchema.model_validate(obj=updated_author)

    async def delete_book(
            self,
            session: AsyncSession,
            book_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_book == book_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise BookNotFound(_id=book_id)
