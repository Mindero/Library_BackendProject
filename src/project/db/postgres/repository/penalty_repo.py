from typing import Type

from sqlalchemy import text, insert, update, delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.project.core.exceptions.PenaltyExceptions import PenaltyNotFound
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.models import Penalty, Readers, BookReader
from src.project.schemas.penaltySchema import PenaltySchema, PenaltyCreateUpdateSchema, PenaltyReaderSchema


class PenaltyRepository:
    _collection: Type[Penalty] = Penalty

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_penalty(
            self,
            session: AsyncSession,
    ) -> list[PenaltySchema]:
        query = select(self._collection)

        penalty = await session.scalars(query)

        return [PenaltySchema.model_validate(obj=val) for val in penalty.all()]

    async def get_all_readers(
            self,
            session: AsyncSession,
    ):
        query = (
            select(Readers.reader_ticket,
                   Readers.name,
                   Readers.phone_number,
                   Readers.email,
                   func.sum(Penalty.payment).label('sum_payment'),
                   func.count(Penalty.payment).label('cnt'))
            .join(BookReader, Penalty.id_book_reader == BookReader.id_book_reader)
            .join(Readers, BookReader.reader_ticket == Readers.reader_ticket)
            .group_by(Readers.reader_ticket, Readers.name, Readers.phone_number, Readers.email)
        )
        result = await session.execute(query)

        rows = result.fetchall()  # Получаем все строки

        return [
            PenaltyReaderSchema(
                reader_ticket=row[0],
                name=row[1],
                phone_number=row[2],
                email=row[3],
                sum_payment=row[4],
                cnt=row[5]
            )
            for row in rows
        ]

    async def get_by_id(
            self,
            session: AsyncSession,
            penalty_id: int
    ) -> PenaltySchema:
        query = select(self._collection).where(self._collection.id_book_reader == penalty_id)

        result = await session.scalar(query)

        if not result:
            raise PenaltyNotFound(_id=penalty_id)

        return PenaltySchema.model_validate(obj=result)

    async def create_penalty(
            self,
            session: AsyncSession,
            penalty: PenaltyCreateUpdateSchema,
    ) -> PenaltySchema:
        query = (
            insert(self._collection)
            .values(penalty.model_dump())
            .returning(self._collection)
        )
        try:
            created_penalty = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound("penalty")

        return PenaltySchema.model_validate(obj=created_penalty)

    async def update_penalty(
            self,
            session: AsyncSession,
            penalty_id: int,
            penalty: PenaltyCreateUpdateSchema,
    ) -> PenaltySchema:
        query = (
            update(self._collection)
            .where(self._collection.id_book_reader == penalty_id)
            .values(penalty.model_dump())
            .returning(self._collection)
        )

        try:
            updated_penalty = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound("penalty")

        if not updated_penalty:
            raise PenaltyNotFound(_id=penalty_id)

        return PenaltySchema.model_validate(obj=updated_penalty)

    async def delete_penalty(
            self,
            session: AsyncSession,
            penalty_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_book_reader == penalty_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise PenaltyNotFound(_id=penalty_id)
