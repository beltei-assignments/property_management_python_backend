from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db, SessionLocal
from app.schemas import property_schema as property_schema
from app.services import property_service as property_service
from app.schemas import property_owner_schema
from app.services import property_owner_service
import os
import uuid
from datetime import datetime

router = APIRouter(tags=["Property management"])
router.prefix = "/properties"


@router.get("/")
def get_all_properties(
    page: int = 1,
    limit: int = 10,
    type: Optional[str] = None,
    status: Optional[str] = None,
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
        type=type,
        status=status,
        search=search,
        location=location,
        price_from=price_from,
        price_to=price_to,
    )

    return result


@router.get("/{property_id}")
def get_property_by_id(property_id: int, db: Session = Depends(get_db)):
    data = property_service.get_property_by_id(db=db, property_id=property_id)

    return data


@router.post("/")
def create_property(
    manager_id: int = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    location: str = Form(...),
    status: str = Form(...),
    type: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # Handle image upload
    image_name = None
    image_url = None

    if image:
        # Generate unique filename
        file_extension = (
            os.path.splitext(image.filename)[1] if image.filename else '.jpg'
        )
        image_name = f"{uuid.uuid4()}{file_extension}"

        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/properties"
        os.makedirs(upload_dir, exist_ok=True)

        # Save file
        file_path = os.path.join(upload_dir, image_name)
        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        # Generate URL (you might want to adjust this based on your server configuration)
        image_url = f"/uploads/properties/{image_name}"

    # Create property data
    property_data = property_schema.PropertyCreate(
        manager_id=manager_id,
        title=title,
        description=description,
        price=price,
        location=location,
        status=status,
        type=type,
        image_name=image_name,
        image_url=image_url,
    )

    property_service.create_property(db=db, payload=property_data)

    return {"success": True}


@router.put("/{property_id}")
def update_property_by_id(
    property_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    location: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # Get existing property data to preserve current image
    existing_property = property_service.get_property_by_id(
        db=db, property_id=property_id
    )

    # Handle image upload if provided
    image_name = existing_property.get("image_name")  # Keep existing image name
    image_url = existing_property.get("image_url")  # Keep existing image URL

    if image:
        # Generate unique filename for new image
        file_extension = (
            os.path.splitext(image.filename)[1] if image.filename else '.jpg'
        )
        image_name = f"{uuid.uuid4()}{file_extension}"

        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/properties"
        os.makedirs(upload_dir, exist_ok=True)

        # Save new file
        file_path = os.path.join(upload_dir, image_name)
        with open(file_path, "wb") as buffer:
            buffer.write(image.file.read())

        # Generate new URL
        image_url = f"/uploads/properties/{image_name}"

    # Create property data for update - only include fields that are provided
    update_data = {}

    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if price is not None:
        update_data["price"] = price
    if location is not None:
        update_data["location"] = location
    if status is not None:
        update_data["status"] = status
    if type is not None:
        update_data["type"] = type
    if image_name is not None:
        update_data["image_name"] = image_name
    if image_url is not None:
        update_data["image_url"] = image_url

    # Create PropertyUpdate schema with only the provided fields
    property_data = property_schema.PropertyUpdate(**update_data)

    property_service.update_property(
        db=db, property_id=property_id, payload=property_data
    )
    return {"success": True}


@router.delete("/{property_id}")
def delete_property_by_id(property_id: int, db: Session = Depends(get_db)):
    property_service.delete_property(db=db, property_id=property_id)
    return {"success": True}


# @router.get("/owners/")
# def get_all_owners(property_id: int = None, db: Session = Depends(get_db)):
#     return property_owner_service.get_all_owners(db=db, property_id=property_id)


# @router.post("/owners")
# def create_owner(
#     payload: property_owner_schema.PropertyOwnerCreate, db: Session = Depends(get_db)
# ):
#     return property_owner_service.create_owner(db=db, payload=payload)


# @router.put("/owners/{property_owner_id}")
# def update_owner(
#     property_owner_id: int,
#     payload: property_owner_schema.PropertyOwnerUpdate,
#     db: Session = Depends(get_db),
# ):
#     return property_owner_service.update_owner(
#         db=db, property_owner_id=property_owner_id, payload=payload
#     )


# @router.delete("/owners/{property_owner_id}")
# def delete_owner(property_owner_id: int, db: Session = Depends(get_db)):
#     return property_owner_service.delete_owner(
#         db=db, property_owner_id=property_owner_id
#     )
