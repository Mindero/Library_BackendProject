from pydantic import BaseModel, ConfigDict


class BookPublisherCreateUpdateSchema(BaseModel):
    id_book: int
    id_publisher: int


class BookPublisherSchema(BookPublisherCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_publisher: int
