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
