from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import property_owner_schema
from app.services import property_owner_service

router = APIRouter(tags=["Property owner management"])
router.prefix = "/properties-owners"


@router.get("/")
def get_all_owners(property_id: int = None, db: Session = Depends(get_db)):
    return property_owner_service.get_all_owners(db=db, property_id=property_id)


@router.post("/")
def create_owner(
    payload: property_owner_schema.PropertyOwnerCreate, db: Session = Depends(get_db)
):
    return property_owner_service.create_owner(db=db, payload=payload)


@router.put("/{property_owner_id}")
def update_owner(
    property_owner_id: int,
    payload: property_owner_schema.PropertyOwnerUpdate,
    db: Session = Depends(get_db),
):
    return property_owner_service.update_owner(
        db=db, property_owner_id=property_owner_id, payload=payload
    )


@router.delete("/{property_owner_id}")
def delete_owner(property_owner_id: int, db: Session = Depends(get_db)):
    return property_owner_service.delete_owner(
        db=db, property_owner_id=property_owner_id
    )
