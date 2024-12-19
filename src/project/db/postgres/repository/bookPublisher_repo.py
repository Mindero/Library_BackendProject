from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.project.core.exceptions.BookPublisherExceptions import BookPublisherNotFound
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.models import BookPublisher, Books, Publishers
from src.project.schemas.bookPublisherSchema import BookPublisherSchema, BookPublisherCreateUpdateSchema, \
    ViewBookPublisherSchema


class BookPublisherRepository:
    _collection: Type[BookPublisher] = BookPublisher

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookPublisher(
            self,
            session: AsyncSession,
    ) -> list[BookPublisherSchema]:
        query = select(self._collection)

        bookPublisher = await session.scalars(query)

        return [BookPublisherSchema.model_validate(obj=val) for val in bookPublisher.all()]

    async def get_all_view_bookPublisher(
            self,
            session: AsyncSession,
    ) -> list[ViewBookPublisherSchema]:
        query = (
            select(
                BookPublisher.id_book_publisher,
                BookPublisher.id_book,
                BookPublisher.id_publisher,
                Books.name.label("book_name"),
                Publishers.name.label("publisher_name")
            )
            .join(Books, Books.id_book == BookPublisher.id_book)
            .join(Publishers, Publishers.id_publisher == BookPublisher.id_publisher)
        )

        results = await session.execute(query)  # Используем execute для получения результата
        rows = results.fetchall()  # Получаем все строки

        return [
            ViewBookPublisherSchema(
                id_book_publisher=row[0],
                id_book=row[1],
                id_publisher=row[2],
                book_name=row[3],
                publisher=row[4],
            )
            for row in rows
        ]


    async def get_by_id(
            self,
            session: AsyncSession,
            bookPublisher_id: int
    ) -> BookPublisherSchema:
        query = select(self._collection).where(self._collection.id_book_publisher == bookPublisher_id)

        result = await session.scalar(query)

        if not result:
            raise BookPublisherNotFound(_id=bookPublisher_id)

        return BookPublisherSchema.model_validate(obj=result)

    async def create_bookPublisher(
            self,
            session: AsyncSession,
            bookPublisher: BookPublisherCreateUpdateSchema,
    ) -> BookPublisherSchema:
        query = (
            insert(self._collection)
            .values(bookPublisher.model_dump())
            .returning(self._collection)
        )

        try:
            created_bookPublisher = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound("book_publisher")

        return BookPublisherSchema.model_validate(obj=created_bookPublisher)

    async def update_bookPublisher(
            self,
            session: AsyncSession,
            bookPublisher_id: int,
            bookPublisher: BookPublisherCreateUpdateSchema,
    ) -> BookPublisherSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_book_publisher == bookPublisher_id)
            .values(bookPublisher.model_dump())
            .returning(self._collection)
        )

        updated_bookPublisher = await session.scalar(query)

        if not updated_bookPublisher:
            raise BookPublisherNotFound(_id=bookPublisher_id)

        return BookPublisherSchema.model_validate(obj=updated_bookPublisher)

    async def delete_bookPublisher(
            self,
            session: AsyncSession,
            bookPublisher_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_book_publisher == bookPublisher_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise BookPublisherNotFound(_id=bookPublisher_id)
