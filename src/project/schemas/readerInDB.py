from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, root_validator


class ReaderCreateUpdateSchema(BaseModel):
    name: str
    email: str
    phone_number: str


class ReaderLoginSchema(BaseModel):
    email: str
    password: str


class ReaderRegisterSchema(ReaderCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    password: str


class ReaderSchema(ReaderRegisterSchema):
    model_config = ConfigDict(from_attributes=True)
    created_date: date


class ReaderInDB(ReaderSchema):
    model_config = ConfigDict(from_attributes=True)

    reader_ticket: int
