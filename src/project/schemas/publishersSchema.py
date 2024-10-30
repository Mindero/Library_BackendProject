from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class PublishersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_publisher: int
    name: str
    inn: str
    country: str
