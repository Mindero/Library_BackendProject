from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookPublisher(Base):
    __tablename__ = "book_publisher"

    id_book_publisher: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("books.id_book", ondelete="CASCADE", onupdate="CASCADE"),
                                         nullable=False)
    id_publisher: Mapped[int] = mapped_column(
        ForeignKey("publishers.id_publisher", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False)

    __table_args__ = (UniqueConstraint('id_book', 'id_publisher', name='_book_publisher_uc'),)
