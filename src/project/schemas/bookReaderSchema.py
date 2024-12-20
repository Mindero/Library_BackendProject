from datetime import date

from pydantic import BaseModel, ConfigDict


class BookReaderCreateUpdateSchemaWithoutId(BaseModel):
    id_instance: int
    borrow_date: date
    end_date: date

class BookReaderCreateUpdateSchema(BaseModel):
    reader_ticket: int
    id_instance: int
    borrow_date: date
    end_date: date


class BookReaderSchema(BookReaderCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_reader: int

class ViewBookReaderSchema(BaseModel):
    id_book_reader: int
    reader_ticket: int
    id_instance: int
    borrow_date: date
    end_date: date
    book_name: str
    publisher_name: str