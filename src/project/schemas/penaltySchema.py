from datetime import date

from pydantic import BaseModel, ConfigDict


class PenaltyCreateUpdateSchema(BaseModel):
    start_time: date
    payment: int


class PenaltySchema(PenaltyCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_reader: int


class PenaltyReaderSchema(BaseModel):
    reader_ticket: int
    name: str
    phone_number: str
    email: str
    sum_payment: int
    cnt: int

