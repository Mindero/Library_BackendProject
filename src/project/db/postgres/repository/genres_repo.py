from typing import Type

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.genre import Genres
from src.project.schemas.genresSchema import GenresSchema


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
