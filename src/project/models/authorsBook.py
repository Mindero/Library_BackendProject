from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class AuthorsBook(Base):
    __tablename__ = "authors_book"

    id_authors_book: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("books.id_book", ondelete="CASCADE", onupdate="CASCADE"))
    id_author: Mapped[int] = mapped_column(ForeignKey("authors.id_author", ondelete="CASCADE", onupdate="CASCADE"))
