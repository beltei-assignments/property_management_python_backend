from pydantic import BaseModel
from typing import Optional
from enum import Enum
from decimal import Decimal


class PropertyStatusEnum(str, Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    RENTED = "rented"


class PropertyTypeEnum(str, Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    VILLA = "villa"
    LAND = "land"
    COMMERCIAL = "commercial"
    OFFICE = "office"
    RETAIL = "retail"
    INDUSTRIAL = "industrial"


class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Decimal
    location: str
    status: PropertyStatusEnum
    type: PropertyTypeEnum

    class Config:
        from_attributes = True


class PropertyCreate(PropertyBase):
    manager_id: int


class PropertyGet(PropertyBase):
    id: int
    manager_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    location: Optional[str] = None
    status: Optional[PropertyStatusEnum] = None
    type: Optional[PropertyTypeEnum] = None
