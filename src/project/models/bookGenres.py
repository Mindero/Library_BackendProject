from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookGenres(Base):
    __tablename__ = "book_genres"

    id_book_genres: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column()
    id_genre: Mapped[int] = mapped_column()
