from fastapi import APIRouter

from src.project.db.postgres.repository.readers_repo import ReadersRepository
from src.project.db.postgres.repository.authors_repo import AuthorsRepository
from src.project.db.postgres.repository.books_repo import BooksRepository
from src.project.db.postgres.repository.genres_repo import GenresRepository
from src.project.db.postgres.repository.publishers_repo import PublishersRepository
from src.project.db.postgres.database import PostgresDatabase
from src.project.schemas.readersSchema import ReadersSchema
from src.project.schemas.authorsSchema import AuthorsSchema
from src.project.schemas.booksSchema import BooksSchema
from src.project.schemas.genresSchema import GenresSchema
from src.project.schemas.publishersSchema import PublishersSchema

router = APIRouter()
@router.get("/all_authors", response_model=list[AuthorsSchema])
async def get_all_authors() -> list[AuthorsSchema]:
    author_repo = AuthorsRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await author_repo.check_connection(session=session)
        all_author = await author_repo.get_all_authors(session=session)

    return all_author