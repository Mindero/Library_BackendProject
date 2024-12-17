from typing import Annotated

from fastapi import Depends, status, HTTPException

from project.api.authorization.hash import oauth2_scheme_login
from project.api.authorization.token_service import fetch_access_token, AUTH_EXCEPTION_MESSAGE
from project.core.exceptions.AuthorizationException import AuthorizationException
from project.db.postgres.database import PostgresDatabase
from project.db.postgres.repository.authorsBook_repo import AuthorsBooksRepository
from project.db.postgres.repository.authors_repo import AuthorsRepository
from project.db.postgres.repository.bookGenres_repo import BookGenresRepository
from project.db.postgres.repository.bookInstance_repo import BookInstanceRepository
from project.db.postgres.repository.bookPublisher_repo import BookPublisherRepository
from project.db.postgres.repository.bookReader_repo import BookReaderRepository
from project.db.postgres.repository.books_repo import BooksRepository
from project.db.postgres.repository.genres_repo import GenreRepository
from project.db.postgres.repository.penalty_repo import PenaltyRepository
from project.db.postgres.repository.publishers_repo import PublishersRepository
from project.db.postgres.repository.readers_repo import ReadersRepository
from project.db.postgres.repository.view_book_repo import ViewBookRepository
from project.schemas.readerInDB import ReaderInDB
from project.schemas.tokenSchema import TokenData

from src.project.core.exceptions.ReaderExceptions import ReaderNotFound

database = PostgresDatabase()

author_repo = AuthorsRepository()
book_repo = BooksRepository()
reader_repo = ReadersRepository()
publisher_repo = PublishersRepository()
penalty_repo = PenaltyRepository()
genre_repo = GenreRepository()
authorsBook_repo = AuthorsBooksRepository()
book_genres_repo = BookGenresRepository()
bookInstance_repo = BookInstanceRepository()
bookPublisher_repo = BookPublisherRepository()
bookReader_repo = BookReaderRepository()
viewBook_repo = ViewBookRepository()


async def get_current_reader(
        token: Annotated[str, Depends(oauth2_scheme_login)],
) -> ReaderInDB:
    tokenData: TokenData = fetch_access_token(token)
    reader_id: int = tokenData.reader_id
    try:
        async with database.session() as session:
            reader = await reader_repo.get_by_id(session=session, reader_id=reader_id)
    except ReaderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return reader


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, reader: Annotated[ReaderInDB, Depends(get_current_reader)]):
        if reader.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions")
