from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.readers_repo import ReadersRepository
from src.project.schemas.readersSchema import ReadersSchema

router = APIRouter()


@router.get("/all_readers", response_model=list[ReadersSchema])
async def get_all_readers() -> list[ReadersSchema]:
    user_repo = ReadersRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_readers = await user_repo.get_all_readers(session=session)

    return all_readers
