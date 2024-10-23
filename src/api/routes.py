from fastapi import APIRouter

from src.db.postgres.repository.readers_repo import ReadersRepository
from src.db.postgres.repository.authors_repo import AuthorsRepository
from src.db.postgres.database import PostgresDatabase
from src.schemas.readersSchema import ReadersSchema
from src.schemas.authorsSchema import AuthorsSchema


router = APIRouter()


@router.get("/all_readers", response_model=list[ReadersSchema])
async def get_all_users() -> list[ReadersSchema]:
    user_repo = ReadersRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await user_repo.check_connection(session=session)
        all_readers = await user_repo.get_all_readers(session=session)

    return all_readers

@router.get("/all_authors", response_model=list[AuthorsSchema])
async def get_all_users() -> list[AuthorsSchema]:
    author_repo = AuthorsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await author_repo.check_connection(session=session)
        all_author = await author_repo.get_all_authors(session=session)

    return all_author