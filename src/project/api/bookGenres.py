from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from project.core.enums.Role import Role
from src.project.api.depends import database, book_genres_repo, RoleChecker
from src.project.core.exceptions.BookGenresExceptions import BookGenresNotFound
from src.project.schemas.bookGenresSchema import BookGenresSchema, BookGenresCreateUpdateSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound

router = APIRouter()


@router.get("/all_book_genres", response_model=list[BookGenresSchema])
async def get_all_book_genres() -> list[BookGenresSchema]:
    async with database.session() as session:
        await book_genres_repo.check_connection(session=session)
        all_book_genres = await book_genres_repo.get_all_bookGenres(session=session)

    return all_book_genres


@router.get("/{bookGenres_id}", response_model=BookGenresSchema)
async def get_bookGenres_by_id(bookGenres_id: int) -> BookGenresSchema:
    try:
        async with database.session() as session:
            bookGenres = await book_genres_repo.get_by_id(session=session, bookGenres_id=bookGenres_id)
    except BookGenresNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bookGenres


@router.post("/add_bookGenres", response_model=BookGenresSchema, status_code=status.HTTP_201_CREATED)
async def add_bookGenres(
        bookGenres_dto: BookGenresCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> BookGenresSchema:
    try:
        async with database.session() as session:
            new_bookGenres = await book_genres_repo.create_bookGenres(session=session, bookGenres=bookGenres_dto)
    except BookGenresNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_bookGenres


@router.put(
    "/update_bookGenres/{bookGenres_id}",
    response_model=BookGenresSchema,
    status_code=status.HTTP_200_OK,
)
async def update_bookGenres(
        bookGenres_id: int,
        bookGenres_dto: BookGenresCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> BookGenresSchema:
    try:
        async with database.session() as session:
            updated_bookGenres = await book_genres_repo.update_bookGenres(
                session=session,
                bookGenres_id=bookGenres_id,
                bookGenres=bookGenres_dto,
            )
    except BookGenresNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return updated_bookGenres


@router.delete("/delete_bookGenres/{bookGenres_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookGenres(
        bookGenres_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN]))]
) -> None:
    try:
        async with database.session() as session:
            bookGenres = await book_genres_repo.delete_bookGenres(session=session, bookGenres_id=bookGenres_id)
    except BookGenresNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return bookGenres
