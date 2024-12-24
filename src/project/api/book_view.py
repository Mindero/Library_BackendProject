import itertools
from typing import Annotated, Optional
import asyncio
from fastapi import APIRouter, HTTPException, status, Depends

from project.core.exceptions.BookExceptions import BookNotFound
from project.schemas.views.viewBookSchema import ViewBookSchema
from src.project.api.depends import database, viewBook_repo, book_repo

router = APIRouter()


@router.get("/all_view_books", response_model=list[ViewBookSchema])
async def get_all_view_books(
        genre: Optional[str] = None,
        name: Optional[str] = None,
        year_left: Optional[int] = None,
        year_right: Optional[int] = None,
) -> list[ViewBookSchema]:
    async with database.session() as session:
        all_books_id = await book_repo.get_all_books(
            session=session,
            genre=genre,
            name=name,
            year_left=year_left,
            year_right=year_right
        )
        tasks = [
            viewBook_repo.get_view_books_by_book_id(session=session, id_book=book.id_book)
            for book in all_books_id
        ]
        # Ожидаем выполнения всех задач
        view_books_nested = await asyncio.gather(*tasks)

        # Разворачиваем вложенные списки в один список
        view_books = list(itertools.chain.from_iterable(view_books_nested))
        return view_books


@router.get("/{name}", response_model=list[ViewBookSchema])
async def get_view_books_by_name(name: str) -> list[ViewBookSchema]:
    async with database.session() as session:
        view_books = await viewBook_repo.get_view_books_by_name(session=session, name=name)
    return view_books


@router.get("/author/{id}", response_model=list[ViewBookSchema])
async def get_view_books_by_author_id(author_id: int):
    try:
        async with database.session() as session:
            view_books = await viewBook_repo.get_view_books_by_author_id(session=session, author_id=author_id)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return view_books
