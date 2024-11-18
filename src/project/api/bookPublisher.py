from fastapi import APIRouter, status, HTTPException

from src.project.api.depends import database, bookPublisher_repo
from src.project.core.exceptions.BookPublisherExceptions import BookPublisherNotFound
from src.project.schemas.bookPublisherSchema import BookPublisherSchema, BookPublisherCreateUpdateSchema

router = APIRouter()


@router.get("/all_book_publisher", response_model=list[BookPublisherSchema])
async def get_all_book_publisher() -> list[BookPublisherSchema]:
    async with database.session() as session:
        await bookPublisher_repo.check_connection(session=session)
        all_book_publisher = await bookPublisher_repo.get_all_bookPublisher(session=session)

    return all_book_publisher


@router.post("/add_bookPublisher", response_model=BookPublisherSchema, status_code=status.HTTP_201_CREATED)
async def add_bookPublisher(
        bookPublisher_dto: BookPublisherCreateUpdateSchema,
) -> BookPublisherSchema:
    try:
        async with database.session() as session:
            new_bookPublisher = await bookPublisher_repo.create_bookPublisher(session=session,
                                                                              bookPublisher=bookPublisher_dto)
    except BookPublisherNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_bookPublisher


@router.put(
    "/update_bookPublisher/{bookPublisher_id}",
    response_model=BookPublisherSchema,
    status_code=status.HTTP_200_OK,
)
async def update_bookPublisher(
        bookPublisher_id: int,
        bookPublisher_dto: BookPublisherCreateUpdateSchema,
) -> BookPublisherSchema:
    try:
        async with database.session() as session:
            updated_bookPublisher = await bookPublisher_repo.update_bookPublisher(
                session=session,
                bookPublisher_id=bookPublisher_id,
                bookPublisher=bookPublisher_dto,
            )
    except BookPublisherNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_bookPublisher


@router.delete("/delete_bookPublisher/{bookPublisher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookPublisher(
        bookPublisher_id: int,
) -> None:
    try:
        async with database.session() as session:
            bookPublisher = await bookPublisher_repo.delete_bookPublisher(session=session,
                                                                          bookPublisher_id=bookPublisher_id)
    except BookPublisherNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return bookPublisher
