from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.genres_repo import GenresRepository
from src.project.schemas.genresSchema import GenresSchema

router = APIRouter()


@router.get("/all_genres", response_model=list[GenresSchema])
async def get_all_genres() -> list[GenresSchema]:
    genres_repo = GenresRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await genres_repo.check_connection(session=session)
        all_genres = await genres_repo.get_all_genres(session=session)

    return all_genres
