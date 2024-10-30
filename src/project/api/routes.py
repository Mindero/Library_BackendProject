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

@router.get("/all_books", response_model=list[BooksSchema])
async def get_all_books() -> list[BooksSchema]:
    book_repo = BooksRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await book_repo.check_connection(session=session)
        all_books = await book_repo.get_all_books(session=session)

    return all_books

@router.get("/all_genres", response_model=list[GenresSchema])
async def get_all_genres() -> list[GenresSchema]:
    genres_repo = GenresRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await genres_repo.check_connection(session=session)
        all_genres = await genres_repo.get_all_genres(session=session)

    return all_genres

@router.get("/all_publishers", response_model=list[PublishersSchema])
async def get_all_publishers() -> list[PublishersSchema]:
    publisher_repo = PublishersRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await publisher_repo.check_connection(session=session)
        all_publishers = await publisher_repo.get_all_publishers(session=session)

    return all_publishers