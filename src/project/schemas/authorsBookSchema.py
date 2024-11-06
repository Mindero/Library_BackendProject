from pydantic import BaseModel, ConfigDict


class AuthorsBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_authors_book: int
    id_book: int
    id_author: int
