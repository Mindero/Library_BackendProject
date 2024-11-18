from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class Penalty(Base):
    __tablename__ = "penalty"

    id_book_reader: Mapped[int] = mapped_column(
        ForeignKey("book_reader.id_book_reader", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True)
    start_time: Mapped[Date] = mapped_column(Date, nullable=False)
    payment: Mapped[int] = mapped_column(nullable=False)
