from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class BookReader(Base):
    __tablename__ = "book_reader"

    id_book_reader: Mapped[int] = mapped_column(primary_key=True)
    reader_ticket: Mapped[int] = mapped_column()
    id_instance: Mapped[int] = mapped_column()
    borrow_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
