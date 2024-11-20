from fastapi import APIRouter, status, HTTPException

from src.project.api.depends import database, bookReader_repo
from src.project.core.exceptions.BookReaderExceptions import BookReaderNotFound
from src.project.schemas.bookReaderSchema import BookReaderSchema, BookReaderCreateUpdateSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound

router = APIRouter()


@router.get("/all_book_reader", response_model=list[BookReaderSchema])
async def get_all_book_reader() -> list[BookReaderSchema]:
    async with database.session() as session:
        await bookReader_repo.check_connection(session=session)
        all_book_reader = await bookReader_repo.get_all_bookReader(session=session)

    return all_book_reader


@router.get("/{bookReader_id}", response_model=BookReaderSchema)
async def get_bookReader_by_id(bookReader_id: int) -> BookReaderSchema:
    try:
        async with database.session() as session:
            bookReader = await bookReader_repo.get_by_id(session=session, bookReader_id=bookReader_id)
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return bookReader


@router.post("/add_bookReader", response_model=BookReaderSchema, status_code=status.HTTP_201_CREATED)
async def add_bookReader(
        bookReader_dto: BookReaderCreateUpdateSchema,
) -> BookReaderSchema:
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
) -> None:
    try:
        async with database.session() as session:
            bookReader = await bookReader_repo.delete_bookReader(session=session, bookReader_id=bookReader_id)
    except BookReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return bookReader
