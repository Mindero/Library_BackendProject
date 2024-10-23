from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.schemas.genresSchema import GenresSchema
from src.models.genre import Genres

from src.core.config import settings


class GenresRepository:
    _collection: Type[Genres] = Genres

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_genres(
        self,
        session: AsyncSession,
    ) -> list[GenresSchema]:
        query = f"select * from {settings.POSTGRES_SCHEMA}.genres;"

        genres = await session.execute(text(query))

        return [GenresSchema.model_validate(obj=genre) for genre in genres.mappings().all()]