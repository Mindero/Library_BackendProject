from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class BooksSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book: int
    name: str
    year: int

