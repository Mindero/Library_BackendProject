from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from project.core.exceptions.BookExceptions import BookNotFound
from project.schemas.views.viewBookSchema import ViewBookSchema
from src.project.api.depends import database, viewBook_repo

router = APIRouter()


@router.get("/all_view_books", response_model=list[ViewBookSchema])
async def get_all_view_books() -> list[ViewBookSchema]:
    async with database.session() as session:
        all_view_books = await viewBook_repo.get_all_view_books(session=session)

    return all_view_books


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
