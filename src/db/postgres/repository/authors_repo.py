from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.schemas.authorsSchema import AuthorsSchema
from src.models.author import Authors

from src.core.config import settings


class AuthorsRepository:
    _collection: Type[Authors] = Authors

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_authors(
        self,
        session: AsyncSession,
    ) -> list[AuthorsSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.authors;"

        authors = await session.execute(text(query))

        return [AuthorsSchema.model_validate(obj=author) for author in authors.mappings().all()]