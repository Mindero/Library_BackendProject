from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.bookInstance_repo import BookInstanceRepository
from src.project.schemas.bookInstanceSchema import BookInstanceSchema

router = APIRouter()


@router.get("/all_book_instance", response_model=list[BookInstanceSchema])
async def get_all_book_instance() -> list[BookInstanceSchema]:
    repo = BookInstanceRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await repo.check_connection(session=session)
        all_book_instance = await repo.get_all_bookInstance(session=session)

    return all_book_instance
