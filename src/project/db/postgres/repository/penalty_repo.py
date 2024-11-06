from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.penalty import Penalty
from src.project.schemas.penaltySchema import PenaltySchema


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
        query = f"select * from {settings.POSTGRES_SCHEMA}.{Penalty.__tablename__};"

        penalty = await session.execute(text(query))

        return [PenaltySchema.model_validate(obj=val) for val in penalty.mappings().all()]
