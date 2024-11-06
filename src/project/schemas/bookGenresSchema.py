from pydantic import BaseModel, ConfigDict


class BookGenresSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book_genres: int
    id_book: int
    id_genre: int
