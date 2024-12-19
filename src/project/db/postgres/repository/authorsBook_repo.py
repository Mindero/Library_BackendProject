from typing import Type

from sqlalchemy import text, insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.project.core.exceptions.AuthorsBookException import AuthorsBookNotFound
from src.project.models import AuthorsBook, Books, Authors
from src.project.schemas.authorsBookSchema import AuthorsBookSchema, AuthorsBookCreateUpdateSchema, \
    ViewAuthorsBookSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound

from pydantic import ValidationError

class AuthorsBooksRepository:
    _collection: Type[AuthorsBook] = AuthorsBook

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_authorsBooks(
            self,
            session: AsyncSession,
    ) -> list[AuthorsBookSchema]:
        query = select(self._collection)

        authorsBooks_books = await session.scalars(query)

        return [AuthorsBookSchema.model_validate(obj=val) for val in authorsBooks_books.all()]

    async def get_all_view_authorsBooks(
            self,
            session: AsyncSession,
    ) -> list[ViewAuthorsBookSchema]:
        query = (
            select(
                AuthorsBook.id_authors_book,
                AuthorsBook.id_book,
                AuthorsBook.id_author,
                Books.name.label("book_name"),
                Authors.name.label("author_name")
            )
            .join(Books, Books.id_book == AuthorsBook.id_book)
            .join(Authors, Authors.id_author == AuthorsBook.id_author)
        )

        results = await session.execute(query)  # Используем execute для получения результата
        rows = results.fetchall()  # Получаем все строки

        return [
            ViewAuthorsBookSchema(
                id_authors_book=row[0],
                id_book=row[1],
                id_author=row[2],
                book_name=row[3],
                author_name=row[4]
            )
            for row in rows
        ]

    async def get_by_id(
            self,
            session: AsyncSession,
            authors_book_id: int
    ) -> AuthorsBookSchema:
        query = select(self._collection).where(self._collection.id_authors_book == authors_book_id)

        result = await session.scalar(query)

        if not result:
            raise AuthorsBookNotFound(_id=authors_book_id)

        return AuthorsBookSchema.model_validate(obj=result)


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

        try:
            created_authorsBook = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound(table_name="authors_book")

        return AuthorsBookSchema.model_validate(obj=created_authorsBook)

    async def update_authorsBook(
            self,
            session: AsyncSession,
            authorsBook_id: int,
            authorsBook: AuthorsBookCreateUpdateSchema,
    ) -> AuthorsBookSchema:
        query = (
            update(self._collection)
            .where(self._collection.id_authors_book == authorsBook_id)
            .values(authorsBook.model_dump())
            .returning(self._collection)
        )

        try:
            updated_authorsBook = await session.scalar(query)
            await session.commit()
        except IntegrityError:
            raise ForeignKeyNotFound(table_name="authors_book")

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
