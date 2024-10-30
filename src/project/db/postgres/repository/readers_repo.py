from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.schemas.readersSchema import ReadersSchema
from src.project.models.reader import Readers

from src.project.core.config import settings


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
    ) -> list[ReadersSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.readers;"

        readers = await session.execute(text(query))

        return [ReadersSchema.model_validate(obj=readers) for readers in readers.mappings().all()]