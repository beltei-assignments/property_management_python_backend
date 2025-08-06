from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db, SessionLocal
from app.schemas import property_schema as property_schema
from app.services import property_service as property_service

router = APIRouter(tags=["Property management"])
router.prefix = "/properties"


@router.get("/")
def get_all_properties(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    location: Optional[str] = None,
    price_from: Optional[float] = None,
    price_to: Optional[float] = None,
    db: Session = Depends(get_db),
):
    result = property_service.get_all_properties(
        db=db, 
        page=page, 
        limit=limit, 
        search=search, 
        location=location, 
        price_from=price_from, 
        price_to=price_to
    )

    return result


@router.get("/{property_id}")
def get_property_by_id(property_id: int, db: Session = Depends(get_db)):
    data = property_service.get_property_by_id(db=db, property_id=property_id)

    return data


@router.post("/")
def create_property(property: property_schema.PropertyCreate, db: Session = Depends(get_db)):
    property_service.create_property(db=db, payload=property)
    return {"success": True}


@router.put("/{property_id}")
def update_property_by_id(
    property_id: int, property: property_schema.PropertyUpdate, db: Session = Depends(get_db)
):
    property_service.update_property(db=db, property_id=property_id, payload=property)
    return {"success": True}


@router.delete("/{property_id}")
def delete_property_by_id(property_id: int, db: Session = Depends(get_db)):
    property_service.delete_property(db=db, property_id=property_id)
    return {"success": True}
