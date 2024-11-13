from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class Authors(Base):
    __tablename__ = "authors"

    id_author: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[Date] = mapped_column(Date, nullable=True)
