from pydantic import BaseModel, ConfigDict


class BooksSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book: int
    name: str
    year: int
