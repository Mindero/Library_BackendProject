from typing import List, Tuple, Dict

from pydantic import BaseModel, ConfigDict


class ViewBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_book: int
    book_name: str
    book_year: int
    authors: List[dict]  # (name id)
