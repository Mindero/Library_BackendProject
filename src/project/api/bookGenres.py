from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.bookGenres_repo import BookGenresRepository
from src.project.schemas.bookGenresSchema import BookGenresSchema

router = APIRouter()


@router.get("/all_book_genres", response_model=list[BookGenresSchema])
async def get_all_book_genres() -> list[BookGenresSchema]:
    book_genres_repo = BookGenresRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await book_genres_repo.check_connection(session=session)
        all_book_genres = await book_genres_repo.get_all_bookGenres(session=session)

    return all_book_genres
