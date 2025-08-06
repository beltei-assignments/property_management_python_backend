from pydantic import BaseModel
from typing import Optional
from datetime import date


class OwnerInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    disabled: bool

    class Config:
        orm_mode = True


class PropertyOwnerBase(BaseModel):
    property_id: int
    owner_id: int
    ownership_start: date
    ownership_end: date


class PropertyOwnerCreate(PropertyOwnerBase):
    pass


class PropertyOwnerUpdate(PropertyOwnerBase):
    pass


class PropertyOwnerGet(PropertyOwnerBase):
    id: int
    owner: OwnerInfo

    class Config:
        orm_mode = True


class PropertyOwnerListResponse(BaseModel):
    count: int
    rows: list[PropertyOwnerGet]
