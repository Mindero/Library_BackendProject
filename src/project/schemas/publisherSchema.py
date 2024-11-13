from pydantic import BaseModel, ConfigDict


class PublisherCreateUpdateSchema(BaseModel):
    name: str
    inn: str
    country: str


class PublisherSchema(PublisherCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    id_publisher: int
