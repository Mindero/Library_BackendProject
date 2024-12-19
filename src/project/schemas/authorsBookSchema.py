from pydantic import BaseModel, ConfigDict


class AuthorsBookCreateUpdateSchema(BaseModel):
    id_book: int
    id_author: int


class AuthorsBookSchema(AuthorsBookCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_authors_book: int

class ViewAuthorsBookSchema(BaseModel):
    id_authors_book: int
    id_book: int
    id_author: int
    book_name: str
    author_name: str