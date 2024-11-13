from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.project.core.config import settings
from src.project.models.genre import Genres
from src.project.schemas.genreSchema import GenreSchema, GenreCreateUpdateSchema
from src.project.core.exceptions.GenreExceptions import GenreAlreadyExists, GenreNotFound

class GenreRepository:
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
    ) -> list[GenreSchema]:
        query = select(self._collection)

        genre = await session.scalars(query)

        return [GenreSchema.model_validate(obj=genre) for genre in genre.all()]

    async def create_genre(
            self,
            session: AsyncSession,
            genre: GenreCreateUpdateSchema,
    ) -> GenreSchema:
        query = (
            insert(self._collection)
            .values(genre.model_dump())
            .returning(self._collection)
        )

        created_genre = await session.scalar(query)
        await session.commit()

        return GenreSchema.model_validate(obj=created_genre)

    async def update_genre(
            self,
            session: AsyncSession,
            genre_id: int,
            genre: GenreCreateUpdateSchema,
    ) -> GenreSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_genre == genre_id)
            .values(genre.model_dump())
            .returning(self._collection)
        )

        try:
            updated_genre = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise GenreAlreadyExists(inn=genre.name)

        return GenreSchema.model_validate(obj=updated_genre)

    async def delete_genre(
            self,
            session: AsyncSession,
            genre_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_genre == genre_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise GenreNotFound(_id=genre_id)