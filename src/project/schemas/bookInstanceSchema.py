from datetime import date

from pydantic import BaseModel, ConfigDict


class BookInstanceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_instance: int
    id_book_publisher: int
    supply_date: date
    taken_now: bool
