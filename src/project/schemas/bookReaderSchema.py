from datetime import date

from pydantic import BaseModel, ConfigDict


class BookReaderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book_reader: int
    reader_ticket: int
    id_instance: int
    borrow_date: date
    end_date: date
