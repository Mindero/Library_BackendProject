from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class Books(Base):
    __tablename__ = "books"

    id_book: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
