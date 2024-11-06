from fastapi import APIRouter

from src.project.db.postgres.database import PostgresDatabase
from src.project.db.postgres.repository.authorsBook_repo import AuthorsBookRepository
from src.project.schemas.authorsBookSchema import AuthorsBookSchema

router = APIRouter()


@router.get("/all_authorsBook", response_model=list[AuthorsBookSchema])
async def get_all_authorsBook() -> list[AuthorsBookSchema]:
    authorsBook_repo = AuthorsBookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await authorsBook_repo.check_connection(session=session)
        all_authorsBook = await authorsBook_repo.get_all_authorsBook(session=session)

    return all_authorsBook
