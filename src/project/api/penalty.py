from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.penalty_repo import PenaltyRepository
from src.project.schemas.penaltySchema import PenaltySchema

router = APIRouter()


@router.get("/all_penalty", response_model=list[PenaltySchema])
async def get_all_penalty() -> list[PenaltySchema]:
    repo = PenaltyRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await repo.check_connection(session=session)
        all_penalty = await repo.get_all_penalty(session=session)

    return all_penalty
