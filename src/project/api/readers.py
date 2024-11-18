from fastapi import APIRouter, status, HTTPException

from src.project.api.depends import database, reader_repo
from src.project.core.exceptions.ReaderExceptions import ReaderNotFound
from src.project.schemas.readerSchema import ReaderSchema, ReaderCreateUpdateSchema

router = APIRouter()


@router.get("/all_readers", response_model=list[ReaderSchema])
async def get_all_readers() -> list[ReaderSchema]:
    async with database.session() as session:
        await reader_repo.check_connection(session=session)
        all_readers = await reader_repo.get_all_readers(session=session)

    return all_readers


@router.post("/add_reader", response_model=ReaderSchema, status_code=status.HTTP_201_CREATED)
async def add_reader(
        reader_dto: ReaderCreateUpdateSchema,
) -> ReaderSchema:
    try:
        async with database.session() as session:
            new_reader = await reader_repo.create_reader(session=session, reader=reader_dto)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_reader


@router.put(
    "/update_reader/{reader_id}",
    response_model=ReaderSchema,
    status_code=status.HTTP_200_OK,
)
async def update_reader(
        reader_id: int,
        reader_dto: ReaderCreateUpdateSchema,
) -> ReaderSchema:
    try:
        async with database.session() as session:
            updated_reader = await reader_repo.update_reader(
                session=session,
                reader_id=reader_id,
                reader=reader_dto,
            )
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_reader


@router.delete("/delete_reader/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reader(
        reader_id: int,
) -> None:
    try:
        async with database.session() as session:
            reader = await reader_repo.delete_reader(session=session, reader_id=reader_id)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return reader
