from pydantic import BaseModel, ConfigDict


class AuthorsBookCreateUpdateSchema(BaseModel):
    id_book: int
    id_author: int


class AuthorsBookSchema(AuthorsBookCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_authors_book: int
