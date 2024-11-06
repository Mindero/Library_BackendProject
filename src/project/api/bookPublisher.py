from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.bookPublisher_repo import BookPublisherRepository
from src.project.schemas.bookPublisherSchema import BookPublisherSchema

router = APIRouter()


@router.get("/all_book_publisher", response_model=list[BookPublisherSchema])
async def get_all_book_publisher() -> list[BookPublisherSchema]:
    repo = BookPublisherRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await repo.check_connection(session=session)
        all_book_publisher = await repo.get_all_bookPublisher(session=session)

    return all_book_publisher
