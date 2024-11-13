from datetime import date

from pydantic import BaseModel, ConfigDict


class ReaderCreateUpdateSchema(BaseModel):
    name: str
    email: str
    phone_number: str
    passport: str
    created_date: date


class ReaderSchema(ReaderCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    reader_ticket: int
