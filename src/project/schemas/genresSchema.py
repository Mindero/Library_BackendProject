from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class GenresSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_genre: int
    name: str

