from typing import Type

from sqlalchemy import text, insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.project.core.config import settings
from src.project.models.authorsBook import AuthorsBook
from src.project.schemas.authorsBookSchema import AuthorsBookSchema, AuthorsBookCreateUpdateSchema
from src.project.core.exceptions.AuthorsBookException import AuthorsBookNotFound

class AuthorsBooksRepository:
    _collection: Type[AuthorsBookSchema] = AuthorsBookSchema

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_authorsBooksBook(
            self,
            session: AsyncSession,
    ) -> list[AuthorsBookSchema]:
        query = select(self._collection)

        authorsBooks_books = await session.scalars(query)

        return [AuthorsBookSchema.model_validate(obj=val) for val in authorsBooks_books.all()]

    async def create_authorsBook(
            self,
            session: AsyncSession,
            authorsBook: AuthorsBookCreateUpdateSchema,
    ) -> AuthorsBookSchema:
        query = (
            insert(self._collection)
            .values(authorsBook.model_dump())
            .returning(self._collection)
        )

        created_authorsBook = await session.scalar(query)

        if not created_authorsBook:
            raise
        await session.commit()

        return AuthorsBookSchema.model_validate(obj=created_authorsBook)

    async def update_authorsBook(
            self,
            session: AsyncSession,
            authorsBook_id: int,
            authorsBook: AuthorsBookCreateUpdateSchema,
    ) -> AuthorsBookSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_authorsBook == authorsBook_id)
            .values(authorsBook.model_dump())
            .returning(self._collection)
        )

        updated_authorsBook = await session.scalar(query)

        if not updated_authorsBook:
            raise AuthorsBookNotFound(_id=authorsBook_id)

        return AuthorsBookSchema.model_validate(obj=updated_authorsBook)

    async def delete_authorsBook(
            self,
            session: AsyncSession,
            authorsBook_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id_authorsBook == authorsBook_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise AuthorsBookNotFound(_id=authorsBook_id)
