from fastapi import APIRouter, HTTPException, status

from src.project.api.depends import database, bookInstance_repo
from src.project.core.exceptions.BookInstanceExceptions import BookInstanceNotFound
from src.project.schemas.bookInstanceSchema import BookInstanceSchema, BookInstanceCreateUpdateSchema

router = APIRouter()


@router.get("/all_book_instance", response_model=list[BookInstanceSchema])
async def get_all_book_instance() -> list[BookInstanceSchema]:
    async with database.session() as session:
        await bookInstance_repo.check_connection(session=session)
        all_book_instance = await bookInstance_repo.get_all_bookInstance(session=session)

    return all_book_instance


@router.post("/add_bookInstance", response_model=BookInstanceSchema, status_code=status.HTTP_201_CREATED)
async def add_bookInstance(
        bookInstance_dto: BookInstanceCreateUpdateSchema,
) -> BookInstanceSchema:
    try:
        async with database.session() as session:
            new_bookInstance = await bookInstance_repo.create_bookInstance(session=session,
                                                                           bookInstance=bookInstance_dto)
    except BookInstanceNotFound as error:
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

    return updated_bookInstance


@router.delete("/delete_bookInstance/{bookInstance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookInstance(
        bookInstance_id: int,
) -> None:
    try:
        async with database.session() as session:
            bookInstance = await bookInstance_repo.delete_bookInstance(session=session, bookInstance_id=bookInstance_id)
    except BookInstanceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return bookInstance
