from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class AuthorsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_author: int
    name: str
    country: str
    birthday: date

