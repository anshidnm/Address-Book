from pydantic import BaseModel, Field
from datetime import datetime


class AddressSchema(BaseModel):
    id: int
    name: str
    latitude: float = Field()
    longitude: float = Field()
    location: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CreateAddressSchema(BaseModel):
    name: str
    latitude: float
    longitude: float
    location: str

class UpdateAddressSchema(BaseModel):
    name: str = None
    latitude: float = None
    longitude: float = None
    location: str = None
