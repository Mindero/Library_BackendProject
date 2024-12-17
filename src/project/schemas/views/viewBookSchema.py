from pydantic import BaseModel, ConfigDict


class ViewBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_authors_book: int
    book_name: str
    author_name: str
    book_year: int
    id_book: int
    id_author: int
