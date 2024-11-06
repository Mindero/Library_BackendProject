from datetime import date

from pydantic import BaseModel, ConfigDict


class PenaltySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book_reader: int
    start_time: date
    payment: int
