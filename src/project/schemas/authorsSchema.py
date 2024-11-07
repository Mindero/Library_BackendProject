from datetime import date

from pydantic import BaseModel, ConfigDict


class AuthorsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_author: int
    name: str
    country: str
    birthday: date