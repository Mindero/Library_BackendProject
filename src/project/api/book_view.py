from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.views.viewBookSchema import ViewBookSchema
from src.project.api.depends import database, viewBook_repo

router = APIRouter()


@router.get("/all_view_books", response_model=list[ViewBookSchema])
async def get_all_view_books() -> list[ViewBookSchema]:
    async with database.session() as session:
        all_view_books = await viewBook_repo.get_all_view_books(session=session)

    return all_view_books
