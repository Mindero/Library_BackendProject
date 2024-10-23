from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date

from  src.db.postgres.database import Base

class Genres(Base):
    __tablename__ = "genres"

    id_genre: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
