from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.project.schemas.publishersSchema import PublishersSchema
from src.project.models.publisher import Publishers

from src.project.core.config import settings


class PublishersRepository:
    _collection: Type[Publishers] = Publishers

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_publishers(
        self,
        session: AsyncSession,
    ) -> list[PublishersSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.publishers;"

        publishers = await session.execute(text(query))

        return [PublishersSchema.model_validate(obj=publisher) for publisher in publishers.mappings().all()]