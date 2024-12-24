from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status, Depends

from src.project.api.depends import database, book_repo, RoleChecker
from src.project.core.exceptions.BookExceptions import BookNotFound
from src.project.schemas.bookSchema import BookSchema, BookCreateUpdateSchema
from src.project.core.enums.Role import Role

router = APIRouter()


@router.get("/all_books", response_model=list[BookSchema])
async def get_all_books() -> list[BookSchema]:
    async with database.session() as session:
        await book_repo.check_connection(session=session)
        all_book = await book_repo.get_all_books(session=session)

    return all_book

@router.post("/add_book", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def add_book(
        book_dto: BookCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> BookSchema:
    try:
        async with database.session() as session:
            new_book = await book_repo.create_book(session=session, book=book_dto)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_book


@router.get("/{book_id}", response_model=BookSchema)
async def get_book_by_id(book_id: int) -> BookSchema:
    try:
        async with database.session() as session:
            book = await book_repo.get_by_id(session=session, book_id=book_id)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return book


@router.put(
    "/update_book/{book_id}",
    response_model=BookSchema,
    status_code=status.HTTP_200_OK,
)
async def update_book(
        book_id: int,
        book_dto: BookCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> BookSchema:
    try:
        async with database.session() as session:
            updated_book = await book_repo.update_book(
                session=session,
                book_id=book_id,
                book=book_dto,
            )
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_book


@router.delete("/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> None:
    try:
        async with database.session() as session:
            book = await book_repo.delete_book(session=session, book_id=book_id)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return book


@router.get("/book_info/{book_id}")
async def get_book_and_authors_by_id(book_id: int):
    try:
        async with database.session() as session:
            book = await book_repo.get_book_and_authors_by_name(session=session, id_book=book_id)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return book
