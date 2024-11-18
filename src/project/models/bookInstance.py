from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookInstance(Base):
    __tablename__ = "book_instance"

    id_instance: Mapped[int] = mapped_column(primary_key=True)
    id_book_publisher: Mapped[int] = mapped_column(ForeignKey("book_publisher.id_book_publisher", ondelete="CASCADE", onupdate="CASCADE"),
                                                   nullable=False)
    supply_date: Mapped[Date] = mapped_column(Date, nullable=False)
    taken_now: Mapped[bool] = mapped_column(nullable=False)
