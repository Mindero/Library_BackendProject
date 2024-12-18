from typing import Type

from sqlalchemy import text, update, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.project.core.config import settings
from src.project.core.exceptions.BookReaderExceptions import BookReaderNotFound
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.models import BookReader, Books, BookInstance, BookPublisher
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
        query = select(self._collection)

        bookReader = await session.scalars(query)
        print("get_all_bookReader")
        return [BookReaderSchema.model_validate(obj=val) for val in bookReader.all()]

    async def get_by_id(
            self,
            session: AsyncSession,
            bookReader_id: int
    ) -> BookReaderSchema:
        query = select(self._collection).where(self._collection.id_book_reader == bookReader_id)

        result = await session.scalar(query)

        if not result:
            raise BookReaderNotFound(_id=bookReader_id)

        return BookReaderSchema.model_validate(obj=result)

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

        try:
            created_bookReader = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound("book_reader")

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

        try:
            updated_bookReader = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound("book_reader")

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

    async def get_all_by_reader_id(
            self,
            session: AsyncSession,
            reader_id: int
    ):
        query = (
            select(Books.name, Books.id_book, BookReader.id_instance, BookReader.borrow_date, BookReader.end_date)
            .join(BookInstance, BookInstance.id_instance == BookReader.id_instance)
            .join(BookPublisher, BookPublisher.id_book_publisher == BookInstance.id_book_publisher)
            .join(Books, Books.id_book == BookPublisher.id_book)
            .where(BookReader.reader_ticket == reader_id)
        )

        result = await session.execute(query)

        return [
            {
                "book_name": row[0],
                "id_book": row[1],
                "id_instance": row[2],
                "borrow_date": row[3],
                "end_date": row[4]
            }
            for row in result]
