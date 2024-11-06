from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class AuthorsBook(Base):
    __tablename__ = "authors_book"

    id_authors_book: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column()
    id_author: Mapped[int] = mapped_column()
