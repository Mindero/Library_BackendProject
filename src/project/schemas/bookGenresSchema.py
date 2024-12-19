from pydantic import BaseModel, ConfigDict


class BookGenresCreateUpdateSchema(BaseModel):
    id_book: int
    id_genre: int


class BookGenresSchema(BookGenresCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_genres: int


class BookGenresViewSchema(BaseModel):
    id_book_genres: int
    id_book: int
    id_genre: int
    book_name: str
    genre_name: str