from typing import Type

from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.exceptions.AuthorExceptions import AuthorNotFound
from src.project.models import Authors
from src.project.schemas.authorSchema import AuthorSchema, AuthorCreateUpdateSchema


class AuthorsRepository:
    _collection: Type[Authors] = Authors

    async def get_all_authors(
            self,
            session: AsyncSession,
    ) -> list[AuthorSchema]:
        query = select(self._collection)

        authors = await session.scalars(query)

        return [AuthorSchema.model_validate(obj=author) for author in authors.all()]

    async def create_author(
            self,
            session: AsyncSession,
            author: AuthorCreateUpdateSchema,
    ) -> AuthorSchema:
        query = (
            insert(self._collection)
            .values(author.model_dump())
            .returning(self._collection)
        )

        created_author = await session.scalar(query)
        await session.commit()

        return AuthorSchema.model_validate(obj=created_author)

    async def update_author(
            self,
            session: AsyncSession,
            author_id: int,
            author: AuthorCreateUpdateSchema,
    ) -> AuthorSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_author == author_id)
            .values(author.model_dump())
            .returning(self._collection)
        )

        updated_author = await session.scalar(query)

        if not updated_author:
            raise AuthorNotFound(_id=author_id)

        return AuthorSchema.model_validate(obj=updated_author)

    async def delete_author(
            self,
            session: AsyncSession,
            author_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_author == author_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise AuthorNotFound(_id=author_id)

    async def get_by_id(
            self,
            session: AsyncSession,
            author_id: int
    ) -> AuthorSchema:
        query = select(self._collection).where(self._collection.id_author == author_id)

        result = await session.scalar(query)

        if not result:
            raise AuthorNotFound(_id=author_id)

        return AuthorSchema.model_validate(obj=result)