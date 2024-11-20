from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.exceptions.ReaderExceptions import ReaderAlreadyExists, ReaderNotFound
from src.project.models.reader import Readers
from src.project.schemas.readerSchema import ReaderSchema, ReaderCreateUpdateSchema


class ReadersRepository:
    _collection: Type[Readers] = Readers

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_readers(
            self,
            session: AsyncSession,
    ) -> list[ReaderSchema]:
        query = select(self._collection)

        readers = await session.scalars(query)

        return [ReaderSchema.model_validate(obj=readers) for readers in readers.all()]


    async def get_by_id(
            self,
            session: AsyncSession,
            reader_id: int
    ) -> ReaderSchema:
        query = select(self._collection).where(self._collection.reader_ticket == reader_id)

        result = await session.scalar(query)

        if not result:
            raise ReaderNotFound(_id=reader_id)

        return ReaderSchema.model_validate(obj=result)


    async def create_reader(
            self,
            session: AsyncSession,
            reader: ReaderCreateUpdateSchema,
    ) -> ReaderSchema:
        query = (
            insert(self._collection)
            .values(reader.model_dump())
            .returning(self._collection)
        )

        try:
            created_reader = await session.scalar(query)
            await session.commit()
        except IntegrityError as e:
            raise ReaderAlreadyExists()

        return ReaderSchema.model_validate(obj=created_reader)

    async def update_reader(
            self,
            session: AsyncSession,
            reader_id: int,
            reader: ReaderCreateUpdateSchema,
    ) -> ReaderSchema:
        query = (
            update(self._collection)
            .where(self._collection.reader_ticket == reader_id)
            .values(reader.model_dump())
            .returning(self._collection)
        )

        updated_reader = await session.scalar(query)

        if not updated_reader:
            raise ReaderNotFound(_id=reader_id)

        return ReaderSchema.model_validate(obj=updated_reader)

    async def delete_reader(
            self,
            session: AsyncSession,
            reader_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.reader_ticket == reader_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise ReaderNotFound(_id=reader_id)
