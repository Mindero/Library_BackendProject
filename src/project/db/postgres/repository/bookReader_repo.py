from datetime import date
from typing import Type, Optional

from sqlalchemy import text, update, delete, insert, select, cast, String, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from project.db.postgres.database import metadata
from project.schemas.penaltySchema import PenaltySchema
from src.project.core.config import settings
from src.project.core.exceptions.BookReaderExceptions import BookReaderNotFound
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.models import BookReader, Books, BookInstance, BookPublisher, Publishers
from src.project.schemas.bookReaderSchema import BookReaderSchema, BookReaderCreateUpdateSchema, ViewBookReaderSchema


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

    async def get_all_view_bookReader(
            self,
            session: AsyncSession,
    ) -> list[ViewBookReaderSchema]:
        query = (
            select(
                BookReader.id_book_reader,
                BookReader.reader_ticket,
                BookReader.id_instance,
                BookReader.borrow_date,
                BookReader.end_date,
                Books.name.label("book_name"),
                Publishers.name.label("publisher_name")
            )
            .join(BookInstance, BookInstance.id_instance == BookReader.id_instance)
            .join(BookPublisher, BookPublisher.id_book_publisher == BookInstance.id_book_publisher)
            .join(Books, Books.id_book == BookPublisher.id_book)
            .join(Publishers, Publishers.id_publisher == BookPublisher.id_publisher)
        )

        results = await session.execute(query)  # Используем execute для получения результата
        rows = results.fetchall()  # Получаем все строки

        return [
            ViewBookReaderSchema(
                id_book_reader=row[0],
                reader_ticket=row[1],
                id_instance=row[2],
                borrow_date=row[3],
                end_date=row[4],
                book_name=row[5],
                publisher_name=row[6],
            )
            for row in rows
        ]

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
            select(BookReader.id_book_reader, Books.name, Books.id_book, BookReader.id_instance, BookReader.borrow_date, BookReader.end_date)
            .join(BookInstance, BookInstance.id_instance == BookReader.id_instance)
            .join(BookPublisher, BookPublisher.id_book_publisher == BookInstance.id_book_publisher)
            .join(Books, Books.id_book == BookPublisher.id_book)
            .where(BookReader.reader_ticket == reader_id)
        )

        result = await session.execute(query)

        return [
            {
                "id_book_reader": row[0],
                "book_name": row[1],
                "id_book": row[2],
                "id_instance": row[3],
                "borrow_date": row[4],
                "end_date": row[5]
            }
            for row in result]

    async def get_all_orders(
            self,
            session: AsyncSession,
            reader_name: Optional[str] = None,
            reader_email: Optional[str] = None,
            reader_ticket: Optional[int] = None,
            book_name: Optional[str] = None,
            publisher_name: Optional[str] = None,
            borrow_date: Optional[date] = None,
            end_date: Optional[date] = None,
    ):
        VIEW = metadata.tables[f"{settings.POSTGRES_SCHEMA}.order_view"]

        query = select(VIEW)
        conditions = []

        if reader_name:
            conditions.append(VIEW.c.reader_name.ilike(f"{reader_name}%"))
        if reader_email:
            conditions.append(VIEW.c.reader_email.ilike(f"{reader_email}%"))
        if reader_ticket:
            conditions.append(cast(VIEW.c.reader_ticket, String).ilike(f"{reader_ticket}%"))
        if book_name:
            conditions.append(VIEW.c.book_name.ilike(f"{book_name}%"))
        if publisher_name:
            conditions.append(VIEW.c.publisher_name.ilike(f"{publisher_name}%"))
        if borrow_date:
            conditions.append(VIEW.c.borrow_date >= borrow_date)
        if end_date:
            conditions.append(VIEW.c.end_date <= end_date)

        if conditions:
            query = query.where(and_(*conditions))

        # print(f"query = {query}")

        result = await session.execute(query)

        res = [dict(row) for row in result.mappings()]

        return res
