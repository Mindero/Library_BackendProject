from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.author import Authors
from src.project.schemas.authorsSchema import AuthorsSchema


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
