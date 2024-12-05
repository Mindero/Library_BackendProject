from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class Readers(Base):
    __tablename__ = "readers"

    reader_ticket: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_date: Mapped[Date] = mapped_column(Date, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)  # Hashed
