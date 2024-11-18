from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.exceptions.BookPublisherExceptions import BookPublisherNotFound
from src.project.models.bookPublisher import BookPublisher
from src.project.schemas.bookPublisherSchema import BookPublisherSchema, BookPublisherCreateUpdateSchema


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

        created_bookPublisher = await session.scalar(query)
        await session.commit()

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
