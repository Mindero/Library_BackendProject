from sqlalchemy.orm import Mapped, mapped_column

from src.project.db.postgres.database import Base


class Publishers(Base):
    __tablename__ = "publishers"

    id_publisher: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    inn: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)

