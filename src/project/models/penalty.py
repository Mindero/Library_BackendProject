from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class Penalty(Base):
    __tablename__ = "penalty"

    id_authors_book: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[Date] = mapped_column(Date, nullable=False)
    payment: Mapped[int] = mapped_column(nullable=False)
