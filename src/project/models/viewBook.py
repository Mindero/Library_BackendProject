from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class ViewBook(Base):
    __tablename__ = "view_book"
    __table_args__ = {"schema": "my_app_schema"}

    id_authors_book: Mapped[int] = mapped_column(primary_key=True)
    book_name: Mapped[str] = mapped_column(nullable=False)
    author_name: Mapped[str] = mapped_column(nullable=False)
    book_year: Mapped[int] = mapped_column(nullable=False)
    id_book: Mapped[int] = mapped_column(nullable=False)
    id_author: Mapped[int] = mapped_column(nullable=False)
