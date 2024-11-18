from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookGenres(Base):
    __tablename__ = "book_genres"

    id_book_genres: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("books.id_book", ondelete="CASCADE", onupdate="CASCADE"))
    id_genre: Mapped[int] = mapped_column(ForeignKey("genres.id_genre", ondelete="CASCADE", onupdate="CASCADE"))
