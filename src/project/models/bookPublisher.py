from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookPublisher(Base):
    __tablename__ = "book_publisher"

    id_book_publisher: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(nullable=False)
    id_publisher: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (UniqueConstraint('id_book', 'id_publisher', name='_book_publisher_uc'),)
