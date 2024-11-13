from fastapi import APIRouter, HTTPException, status

from src.project.schemas.bookSchema import BookSchema, BookCreateUpdateSchema
from src.project.api.depends import database, book_repo
from src.project.core.exceptions.BookExceptions import BookNotFound

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
) -> BookSchema:
    try:
        async with database.session() as session:
            new_book = await book_repo.create_book(session=session, book=book_dto)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_book


@router.put(
    "/update_book/{book_id}",
    response_model=BookSchema,
    status_code=status.HTTP_200_OK,
)
async def update_book(
        book_id: int,
        book_dto: BookCreateUpdateSchema,
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
) -> None:
    try:
        async with database.session() as session:
            book = await book_repo.delete_book(session=session, book_id=book_id)
    except BookNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return book
