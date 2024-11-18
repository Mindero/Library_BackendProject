from datetime import date

from pydantic import BaseModel, ConfigDict


class BookInstanceCreateUpdateSchema(BaseModel):
    id_book_publisher: int
    supply_date: date
    taken_now: bool


class BookInstanceSchema(BookInstanceCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_instance: int
