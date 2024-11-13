from datetime import date

from pydantic import BaseModel, ConfigDict


class BookReaderCreateUpdateSchema(BaseModel):
    reader_ticket: int
    id_instance: int
    borrow_date: date
    end_date: date

class BookReaderSchema(BookReaderCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_book_reader: int
