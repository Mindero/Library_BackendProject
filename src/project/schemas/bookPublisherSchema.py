from pydantic import BaseModel, ConfigDict


class BookPublisherSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book_publisher: int
    id_book: int
    id_publisher: int
