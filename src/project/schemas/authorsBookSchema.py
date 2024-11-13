from pydantic import BaseModel, ConfigDict, Field


class AuthorsBookCreateUpdateSchema(BaseModel):
    id_book: int | None = Field(default=None)
    id_author: int | None = Field(default=None)


class AuthorsBookSchema(AuthorsBookCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_authors_book: int
