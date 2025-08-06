from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from fastapi import HTTPException
from app.models.property_model import Property, PropertyStatus, PropertyType
from app.models.user_model import User
from app.schemas.property_schema import PropertyCreate, PropertyUpdate, PropertyStatusEnum, PropertyTypeEnum
from decimal import Decimal

def get_all_properties(db: Session, page: int = 1, limit: int = 10, search: str = None, location: str = None, price_from: float = None, price_to: float = None):
    query = db.query(Property).filter(Property.disabled == False)

    if search:
        query = query.filter(or_(Property.title.ilike(f"%{search}%"), Property.description.ilike(f"%{search}%")))
    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))
    if price_from is not None:
        query = query.filter(Property.price >= Decimal(price_from))
    if price_to is not None:
        query = query.filter(Property.price <= Decimal(price_to))

    count = query.count()
    properties = query.options(joinedload(Property.manager)).offset((page - 1) * limit).limit(limit).all()

    rows = [serialize_property_with_manager(p) for p in properties]
    return {"count": count, "rows": rows}

def get_property_by_id(db: Session, property_id: int):
    property = db.query(Property).options(joinedload(Property.manager)).filter(Property.id == property_id, Property.disabled == False).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return serialize_property_with_manager(property)

def create_property(db: Session, payload: PropertyCreate):
    manager = db.query(User).filter(User.id == payload.manager_id, User.disabled == False).first()
    if not manager:
        raise HTTPException(status_code=400, detail="Manager not found")
    new_property = Property(**payload.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return {"success": True}

def update_property(db: Session, property_id: int, payload: PropertyUpdate):
    property = db.query(Property).filter(Property.id == property_id, Property.disabled == False).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(property, key, value)
    db.commit()
    return {"success": True}

def delete_property(db: Session, property_id: int):
    property = db.query(Property).filter(Property.id == property_id, Property.disabled == False).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    property.disabled = True
    db.commit()
    return {"success": True}

def serialize_property_with_manager(property: Property):
    manager = property.manager if hasattr(property, 'manager') else None
    return {
        "id": property.id,
        "title": property.title,
        "description": property.description,
        "price": float(property.price),
        "location": property.location,
        "status": property.status.value if property.status else None,
        "type": property.type.value if property.type else None,
        "created_at": property.created_at,
        "updated_at": property.updated_at,
        "disabled": getattr(property, 'disabled', False),
        "manager": {
            "id": manager.id,
            "email": manager.email,
            "first_name": manager.first_name,
            "last_name": manager.last_name,
            "phone_number": manager.phone_number,
            "disabled": manager.disabled,
        } if manager else None
    } 