from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, status, Depends

from project.core.exceptions.BookExceptions import BookNotFound
from src.project.api.depends import database, bookInstance_repo, RoleChecker
from src.project.core.exceptions.BookInstanceExceptions import BookInstanceNotFound
from src.project.schemas.bookInstanceSchema import BookInstanceSchema, BookInstanceCreateUpdateSchema, \
    ViewBookInstanceSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.core.enums.Role import Role

router = APIRouter()


@router.get("/all_book_instance", response_model=list[BookInstanceSchema])
async def get_all_book_instance() -> list[BookInstanceSchema]:
    async with database.session() as session:
        await bookInstance_repo.check_connection(session=session)
        all_book_instance = await bookInstance_repo.get_all_bookInstance(session=session)

    return all_book_instance


@router.get("/all_view_book_instance", response_model=list[ViewBookInstanceSchema])
async def get_all_book_instance() -> list[BookInstanceSchema]:
    async with database.session() as session:
        await bookInstance_repo.check_connection(session=session)
        all_book_instance = await bookInstance_repo.get_all_view_bookInstance(session=session)

    return all_book_instance


@router.get("/get_by_id/{bookInstance_id}", response_model=BookInstanceSchema)
async def get_bookInstance_by_id(bookInstance_id: int) -> BookInstanceSchema:
    try:
        async with database.session() as session:
            bookInstance = await bookInstance_repo.get_by_id(session=session, bookInstance_id=bookInstance_id)
    except BookInstanceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bookInstance


@router.post("/add_bookInstance", response_model=BookInstanceSchema, status_code=status.HTTP_201_CREATED)
async def add_bookInstance(
        bookInstance_dto: BookInstanceCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> BookInstanceSchema:
    try:
        async with database.session() as session:
            new_bookInstance = await bookInstance_repo.create_bookInstance(session=session,
                                                                           bookInstance=bookInstance_dto)
    except BookInstanceNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_bookInstance


@router.put(
    "/update_bookInstance/{bookInstance_id}",
    response_model=BookInstanceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_bookInstance(
        bookInstance_id: int,
        bookInstance_dto: BookInstanceCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> BookInstanceSchema:
    try:
        async with database.session() as session:
            updated_bookInstance = await bookInstance_repo.update_bookInstance(
                session=session,
                bookInstance_id=bookInstance_id,
                bookInstance=bookInstance_dto,
            )
    except BookInstanceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return updated_bookInstance


@router.delete("/delete_bookInstance/{bookInstance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookInstance(
        bookInstance_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> None:
    try:
        async with database.session() as session:
            bookInstance = await bookInstance_repo.delete_bookInstance(session=session, bookInstance_id=bookInstance_id)
    except BookInstanceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return bookInstance


@router.get("/get_free_instances/{book_id}", status_code=status.HTTP_200_OK)
async def get_available_instances_by_book_id(
        book_id: int,
):
    try:
        async with database.session() as session:
            instances = await bookInstance_repo.get_available_instances_by_book_id(session=session,
                                                                                   book_id=book_id)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return instances


@router.get("/get_supply_books", status_code=status.HTTP_200_OK)
async def get_supply_books(
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        book_name: Optional[str] = None,
        author_name: Optional[str] = None,
):
    async with database.session() as session:
        result = await bookInstance_repo.get_supply_books(
            session=session,
            start_date=start_date,
            end_date=end_date,
            book_name=book_name,
            author_name=author_name,
        )
    return result
