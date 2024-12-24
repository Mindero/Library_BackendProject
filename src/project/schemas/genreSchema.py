from pydantic import BaseModel, ConfigDict


class GenreCreateUpdateSchema(BaseModel):
    name: str
    url: str


class GenreSchema(GenreCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_genre: int
