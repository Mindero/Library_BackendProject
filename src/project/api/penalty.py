from fastapi import APIRouter, HTTPException, status

from src.project.api.depends import database, penalty_repo
from src.project.core.exceptions.PenaltyExceptions import PenaltyNotFound
from src.project.schemas.penaltySchema import PenaltySchema, PenaltyCreateUpdateSchema

router = APIRouter()


@router.get("/all_penalty", response_model=list[PenaltySchema])
async def get_all_penalty() -> list[PenaltySchema]:
    async with database.session() as session:
        await penalty_repo.check_connection(session=session)
        all_penalty = await penalty_repo.get_all_penalty(session=session)

    return all_penalty


@router.get("/{penalty_id}", response_model=PenaltySchema)
async def get_penalty_by_id(penalty_id: int) -> PenaltySchema:
    try:
        async with database.session() as session:
            penalty = await penalty_repo.get_by_id(session=session, penalty_id=penalty_id)
    except PenaltyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return penalty


@router.post("/add_penalty", response_model=PenaltySchema, status_code=status.HTTP_201_CREATED)
async def add_penalty(
        penalty_dto: PenaltyCreateUpdateSchema,
) -> PenaltySchema:
    try:
        async with database.session() as session:
            new_penalty = await penalty_repo.create_penalty(session=session, penalty=penalty_dto)
    except PenaltyNotFound as error:
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

    return updated_penalty


@router.delete("/delete_penalty/{penalty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_penalty(
        penalty_id: int,
) -> None:
    try:
        async with database.session() as session:
            penalty = await penalty_repo.delete_penalty(session=session, penalty_id=penalty_id)
    except PenaltyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return penalty
