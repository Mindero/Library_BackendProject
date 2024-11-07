from datetime import date

from pydantic import BaseModel, ConfigDict


class ReadersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reader_ticket: int
    name: str
    email: str
    phone_number: str
    passport: str
    created_date: date