from typing import Type

from sqlalchemy import text, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.core.exceptions.BookReaderExceptions import BookReaderNotFound
from src.project.models.bookReader import BookReader
from src.project.schemas.bookReaderSchema import BookReaderSchema, BookReaderCreateUpdateSchema


class BookReaderRepository:
    _collection: Type[BookReader] = BookReader

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_bookReader(
            self,
            session: AsyncSession,
    ) -> list[BookReaderSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.{BookReader.__tablename__};"

        bookReader = await session.execute(text(query))

        return [BookReaderSchema.model_validate(obj=val) for val in bookReader.mappings().all()]

    async def create_bookReader(
            self,
            session: AsyncSession,
            bookReader: BookReaderCreateUpdateSchema,
    ) -> BookReaderSchema:
        query = (
            insert(self._collection)
            .values(bookReader.model_dump())
            .returning(self._collection)
        )

        created_bookReader = await session.scalar(query)
        await session.commit()

        return BookReaderSchema.model_validate(obj=created_bookReader)

    async def update_bookReader(
            self,
            session: AsyncSession,
            bookReader_id: int,
            bookReader: BookReaderCreateUpdateSchema,
    ) -> BookReaderSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_book_reader == bookReader_id)
            .values(bookReader.model_dump())
            .returning(self._collection)
        )

        updated_bookReader = await session.scalar(query)

        if not updated_bookReader:
            raise BookReaderNotFound(_id=bookReader_id)

        return BookReaderSchema.model_validate(obj=updated_bookReader)

    async def delete_bookReader(
            self,
            session: AsyncSession,
            bookReader_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_book_reader == bookReader_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise BookReaderNotFound(_id=bookReader_id)
