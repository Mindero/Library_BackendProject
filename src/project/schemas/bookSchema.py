from pydantic import BaseModel, ConfigDict


class BookCreateUpdateSchema(BaseModel):
    name: str
    year: int


class BookSchema(BookCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book: int
