from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.authors_repo import AuthorsRepository
from src.project.schemas.authorsSchema import AuthorsSchema

router = APIRouter()


@router.get("/all_authors", response_model=list[AuthorsSchema])
async def get_all_authors() -> list[AuthorsSchema]:
    author_repo = AuthorsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await author_repo.check_connection(session=session)
        all_author = await author_repo.get_all_authors(session=session)

    return all_author
