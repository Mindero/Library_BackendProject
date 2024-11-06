from pydantic import BaseModel, ConfigDict


class GenresSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_genre: int
    name: str
