from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.property_owner_model import PropertyOwner
from app.models.user_model import User
from app.schemas.property_owner_schema import PropertyOwnerCreate, PropertyOwnerUpdate


def get_all_owners(db: Session, property_id: int = None):
    query = db.query(PropertyOwner).options(joinedload(PropertyOwner.owner))
    if property_id:
        query = query.filter(PropertyOwner.property_id == property_id)
    count = query.count()
    owners = query.all()
    return {"count": count, "rows": [serialize_property_owner(o) for o in owners]}


def create_owner(db: Session, payload: PropertyOwnerCreate):
    owner = PropertyOwner(**payload.dict())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return {"success": True}


def update_owner(db: Session, property_owner_id: int, payload: PropertyOwnerUpdate):
    owner = (
        db.query(PropertyOwner).filter(PropertyOwner.id == property_owner_id).first()
    )
    if not owner:
        raise HTTPException(status_code=404, detail="Property owner not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(owner, key, value)
    db.commit()
    return {"success": True}


def delete_owner(db: Session, property_owner_id: int):
    owner = (
        db.query(PropertyOwner).filter(PropertyOwner.id == property_owner_id).first()
    )
    if not owner:
        raise HTTPException(status_code=404, detail="Property owner not found")
    db.delete(owner)
    db.commit()
    return {"success": True}


def serialize_property_owner(owner: PropertyOwner):
    return {
        "id": owner.id,
        "property_id": owner.property_id,
        "owner_id": owner.owner_id,
        "ownership_start": owner.ownership_start,
        "ownership_end": owner.ownership_end,
        "owner": (
            {
                "id": owner.owner.id,
                "email": owner.owner.email,
                "first_name": owner.owner.first_name,
                "last_name": owner.owner.last_name,
                "phone_number": owner.owner.phone_number,
                "disabled": owner.owner.disabled,
            }
            if owner.owner
            else None
        ),
    }
