from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.bookReader_repo import BookReaderRepository
from src.project.schemas.bookReaderSchema import BookReaderSchema

router = APIRouter()


@router.get("/all_book_reader", response_model=list[BookReaderSchema])
async def get_all_book_reader() -> list[BookReaderSchema]:
    repo = BookReaderRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await repo.check_connection(session=session)
        all_book_reader = await repo.get_all_bookReader(session=session)

    return all_book_reader
