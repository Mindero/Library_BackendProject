from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AuthorCreateUpdateSchema(BaseModel):
    name: str
    country: str
    birthday: date | None = Field(default=None)


class AuthorSchema(AuthorCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_author: int
