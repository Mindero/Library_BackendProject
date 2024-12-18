import itertools
from typing import Type
import asyncio
from sqlalchemy import text, select, insert, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from project.core.config import settings
from project.db.postgres.database import metadata
from project.schemas.views.viewBookSchema import ViewBookSchema


class ViewBookRepository:

    async def get_all_view_books(
            self,
            session: AsyncSession,
    ) -> list[ViewBookSchema]:
        VIEW = metadata.tables[f"{settings.POSTGRES_SCHEMA}.view_book"]
        query = select(
            VIEW.c.id_book,
            VIEW.c.book_name,
            VIEW.c.book_year,
            func.array_agg(
                func.jsonb_build_object('id', VIEW.c.id_author, 'name', VIEW.c.author_name)
            ).label('authors')
        ).group_by(
            VIEW.c.id_book, VIEW.c.book_name, VIEW.c.book_year
        )

        view_books = await session.execute(query)
        # print("PRINT")
        # print([view_book for view_book in view_books.all()])
        return [
            ViewBookSchema(
                id_book=row[0],
                book_name=row[1],
                book_year=row[2],
                authors=row[3]
            )
            for row in view_books.all()
        ]

    async def get_view_books_by_name(
            self,
            session: AsyncSession,
            name: str,
    ) -> list[ViewBookSchema]:
        VIEW = metadata.tables[f"{settings.POSTGRES_SCHEMA}.view_book"]
        # Запрос для извлечения данных по имени книги
        query = select(
            VIEW.c.id_book,
            VIEW.c.book_name,
            VIEW.c.book_year,
            func.array_agg(
                func.jsonb_build_object('id', VIEW.c.id_author, 'name', VIEW.c.author_name)
            ).label('authors')
        ).where(VIEW.c.book_name == name).group_by(
            VIEW.c.id_book, VIEW.c.book_name, VIEW.c.book_year
        )

        # Выполнение запроса
        result = await session.execute(query)

        # Преобразуем каждую строку результата в словарь и передаем в Pydantic модель
        return [
            ViewBookSchema(
                id_book=row[0],
                book_name=row[1],
                book_year=row[2],
                authors=row[3]
            )
            for row in result.all()
        ]

    async def get_view_books_by_book_id(
            self,
            session: AsyncSession,
            id_book: int,
    ) -> list[ViewBookSchema]:
        VIEW = metadata.tables[f"{settings.POSTGRES_SCHEMA}.view_book"]
        # Запрос для извлечения данных по имени книги
        query = select(
            VIEW.c.id_book,
            VIEW.c.book_name,
            VIEW.c.book_year,
            func.array_agg(
                func.jsonb_build_object('id', VIEW.c.id_author, 'name', VIEW.c.author_name)
            ).label('authors')
        ).where(VIEW.c.id_book == id_book).group_by(
            VIEW.c.id_book, VIEW.c.book_name, VIEW.c.book_year
        )

        # Выполнение запроса
        result = await session.execute(query)

        # Преобразуем каждую строку результата в словарь и передаем в Pydantic модель
        return [
            ViewBookSchema(
                id_book=row[0],
                book_name=row[1],
                book_year=row[2],
                authors=row[3]
            )
            for row in result.all()
        ]

    async def get_view_books_by_author_id(
            self,
            session: AsyncSession,
            author_id: int,
    ) -> list[ViewBookSchema]:
        VIEW = metadata.tables[f"{settings.POSTGRES_SCHEMA}.view_book"]

        # Выполняем запрос для получения всех id книг для данного автора
        query = select(VIEW.c.id_book).where(VIEW.c.id_author == author_id)
        result = await session.execute(query)

        view_id_books = result.scalars().all()

        # Создаем список асинхронных операций для получения книг и их авторов
        # Запускаем асинхронные операции параллельно
        tasks = [
            self.get_view_books_by_book_id(session=session, id_book=id_book)
            for id_book in view_id_books
        ]

        # Ожидаем выполнения всех задач
        view_books_nested = await asyncio.gather(*tasks)

        # Разворачиваем вложенные списки в один список
        view_books = list(itertools.chain.from_iterable(view_books_nested))
        print(f"VIEW_BOOKS: {view_books}")
        return view_books
