from typing import Type

from sqlalchemy import text, insert, update, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.exceptions.GenreExceptions import GenreAlreadyExists, GenreNotFound
from src.project.models import Genres
from src.project.schemas.genreSchema import GenreSchema, GenreCreateUpdateSchema


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

    async def get_by_id(
            self,
            session: AsyncSession,
            genre_id: int
    ) -> GenreSchema:
        query = select(self._collection).where(self._collection.id_genre == genre_id)

        result = await session.scalar(query)

        if not result:
            raise GenreNotFound(_id=genre_id)

        return GenreSchema.model_validate(obj=result)

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

        try:
            created_genre = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise GenreAlreadyExists(name=genre.name)

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
            raise GenreAlreadyExists(name=genre.name)

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
