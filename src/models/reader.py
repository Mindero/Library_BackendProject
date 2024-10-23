from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date

from  src.db.postgres.database import Base

class Readers(Base):
    __tablename__ = "readers"

    id_author: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    birthday: Mapped[Date] = mapped_column(Date)

