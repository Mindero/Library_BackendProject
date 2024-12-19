from pydantic import BaseModel, ConfigDict


class BookPublisherCreateUpdateSchema(BaseModel):
    id_book: int
    id_publisher: int


class BookPublisherSchema(BookPublisherCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_publisher: int

class ViewBookPublisherSchema(BaseModel):
    id_book_publisher: int
    id_book: int
    id_publisher: int
    book_name:str
    publisher:str
