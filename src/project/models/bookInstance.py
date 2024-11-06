from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookInstance(Base):
    __tablename__ = "book_instance"

    id_instance: Mapped[int] = mapped_column(primary_key=True)
    id_book_publisher: Mapped[int] = mapped_column(nullable=False)
    supply_date: Mapped[Date] = mapped_column(Date, nullable=False)
    taken_now: Mapped[bool] = mapped_column(nullable=False)
