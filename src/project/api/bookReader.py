from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from project.schemas.readerInDB import ReaderInDB
from src.project.api.depends import database, bookReader_repo, RoleChecker, get_current_reader
from src.project.core.exceptions.BookReaderExceptions import BookReaderNotFound
from src.project.schemas.bookReaderSchema import BookReaderSchema, BookReaderCreateUpdateSchema, \
    BookReaderCreateUpdateSchemaWithoutId, ViewBookReaderSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.core.enums.Role import Role

router = APIRouter()


@router.get("/all_book_reader", response_model=list[BookReaderSchema])
async def get_all_book_reader(
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> list[BookReaderSchema]:
    async with database.session() as session:
        await bookReader_repo.check_connection(session=session)
        all_book_reader = await bookReader_repo.get_all_bookReader(session=session)

    return all_book_reader

@router.get("/all_view_book_reader", response_model=list[ViewBookReaderSchema])
async def get_all_view_book_reader(
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))]
) -> list[ViewBookReaderSchema]:
    async with database.session() as session:
        await bookReader_repo.check_connection(session=session)
        all_book_reader = await bookReader_repo.get_all_view_bookReader(session=session)

    return all_book_reader

@router.get("/{bookReader_id}", response_model=BookReaderSchema)
async def get_bookReader_by_id(
        bookReader_id: int,
        reader: ReaderInDB = Depends(get_current_reader)
) -> BookReaderSchema:
    try:
        async with database.session() as session:
            bookReader = await bookReader_repo.get_by_id(session=session, bookReader_id=bookReader_id)
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    if bookReader.reader_ticket != reader.reader_ticket and reader.role.value != Role.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions")
    return bookReader


@router.post("/add_bookReader", response_model=BookReaderSchema, status_code=status.HTTP_201_CREATED)
async def add_bookReader(
        bookReader_dto: BookReaderCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
) -> BookReaderSchema:
    try:
        async with database.session() as session:
            new_bookReader = await bookReader_repo.create_bookReader(session=session, bookReader=bookReader_dto)
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_bookReader


@router.patch("/add_bookReader", response_model=BookReaderSchema, status_code=status.HTTP_201_CREATED)
async def add_bookReader(
        bookReaderWithoutId_dto: BookReaderCreateUpdateSchemaWithoutId,
        reader: ReaderInDB = Depends(get_current_reader),
) -> BookReaderSchema:
    bookReader_dto = BookReaderCreateUpdateSchema(
        reader_ticket=reader.reader_ticket,
        id_instance=bookReaderWithoutId_dto.id_instance,
        borrow_date=bookReaderWithoutId_dto.borrow_date,
        end_date=bookReaderWithoutId_dto.end_date,
    )
    try:
        async with database.session() as session:
            new_bookReader = await bookReader_repo.create_bookReader(session=session, bookReader=bookReader_dto)
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_bookReader


@router.put(
    "/update_bookReader/{bookReader_id}",
    response_model=BookReaderSchema,
    status_code=status.HTTP_200_OK,
)
async def update_bookReader(
        bookReader_id: int,
        bookReader_dto: BookReaderCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
) -> BookReaderSchema:
    try:
        async with database.session() as session:
            updated_bookReader = await bookReader_repo.update_bookReader(
                session=session,
                bookReader_id=bookReader_id,
                bookReader=bookReader_dto,
            )
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return updated_bookReader


@router.delete("/delete_bookReader/{bookReader_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookReader(
        bookReader_id: int,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
) -> None:
    try:
        async with database.session() as session:
            bookReader = await bookReader_repo.delete_bookReader(session=session, bookReader_id=bookReader_id)
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bookReader


@router.get("/profile_books/", status_code=status.HTTP_200_OK)
async def profile_books(
        reader: ReaderInDB = Depends(get_current_reader)
):
    async with database.session() as session:
        books = await bookReader_repo.get_all_by_reader_id(session=session, reader_id=reader.reader_ticket)
    return books
