from pydantic import BaseModel, ConfigDict


class BookGenresCreateUpdateSchema(BaseModel):
    id_book: int
    id_genre: int


class BookGenresSchema(BookGenresCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_genres: int
