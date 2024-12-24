from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from project.api.bookReader import get_bookReader_by_id
from project.schemas.readerInDB import ReaderInDB
from src.project.api.depends import database, penalty_repo, RoleChecker, get_current_reader
from src.project.core.exceptions.PenaltyExceptions import PenaltyNotFound
from src.project.schemas.penaltySchema import PenaltySchema, PenaltyCreateUpdateSchema
from src.project.core.exceptions.ForeignKeyNotFound import ForeignKeyNotFound
from src.project.core.enums.Role import Role

router = APIRouter()


@router.get("/all_penalty", response_model=list[PenaltySchema])
async def get_all_penalty(
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
) -> list[PenaltySchema]:
    async with database.session() as session:
        await penalty_repo.check_connection(session=session)
        all_penalty = await penalty_repo.get_all_penalty(session=session)

    return all_penalty

@router.get("/get_all_readers")
async def get_all_penalty(
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
):
    async with database.session() as session:
        await penalty_repo.check_connection(session=session)
        all_penalty = await penalty_repo.get_all_readers(session=session)

    return all_penalty


@router.get("/{penalty_id}", response_model=PenaltySchema)
async def get_penalty_by_id(
        penalty_id: int,
        reader: ReaderInDB = Depends(get_current_reader),
) -> PenaltySchema:
    try:
        async with database.session() as session:
            penalty = await penalty_repo.get_by_id(session=session, penalty_id=penalty_id)
    except PenaltyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    await get_bookReader_by_id(bookReader_id=penalty.id_book_reader, reader=reader)
    return penalty


@router.post("/add_penalty", response_model=PenaltySchema, status_code=status.HTTP_201_CREATED)
async def add_penalty(
        penalty_dto: PenaltySchema,
        reader: ReaderInDB = Depends(get_current_reader),
) -> PenaltySchema:
    await get_bookReader_by_id(bookReader_id=penalty_dto.id_book_reader, reader=reader)
    try:
        async with database.session() as session:
            new_penalty = await penalty_repo.create_penalty(session=session, penalty=penalty_dto)
    except PenaltyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_penalty


@router.put(
    "/update_penalty/{penalty_id}",
    response_model=PenaltySchema,
    status_code=status.HTTP_200_OK,
)
async def update_penalty(
        penalty_id: int,
        penalty_dto: PenaltyCreateUpdateSchema,
        _: Annotated[bool, Depends(RoleChecker(allowed_roles=[Role.ADMIN.value]))],
) -> PenaltySchema:
    try:
        async with database.session() as session:
            updated_penalty = await penalty_repo.update_penalty(
                session=session,
                penalty_id=penalty_id,
                penalty=penalty_dto,
            )
    except PenaltyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except ForeignKeyNotFound as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return updated_penalty


@router.delete("/delete_penalty/{penalty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_penalty(
        penalty_id: int,
        reader: ReaderInDB = Depends(get_current_reader),
) -> None:
    penalty: PenaltySchema = await get_penalty_by_id(penalty_id=penalty_id, reader=reader)
    await get_bookReader_by_id(bookReader_id=penalty.id_book_reader, reader=reader)
    try:
        async with database.session() as session:
            await penalty_repo.delete_penalty(session=session, penalty_id=penalty_id)
    except PenaltyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
