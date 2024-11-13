from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.penalty import Penalty
from src.project.schemas.penaltySchema import PenaltySchema, PenaltyCreateUpdateSchema
from src.project.core.exceptions.PenaltyExceptions import PenaltyNotFound

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

        created_penalty = await session.scalar(query)
        await session.commit()

        return PenaltySchema.model_validate(obj=created_penalty)

    async def update_penalty(
            self,
            session: AsyncSession,
            penalty_id: int,
            penalty: PenaltyCreateUpdateSchema,
    ) -> PenaltySchema:
        query = (
            update(self._collection)
            .where(self._collection.id_authors_book == penalty_id)
            .values(penalty.model_dump())
            .returning(self._collection)
        )

        updated_penalty = await session.scalar(query)

        if not updated_penalty:
            raise PenaltyNotFound(_id=penalty_id)

        return PenaltySchema.model_validate(obj=updated_penalty)

    async def delete_penalty(
            self,
            session: AsyncSession,
            penalty_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_authors_book == penalty_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise PenaltyNotFound(_id=penalty_id)
