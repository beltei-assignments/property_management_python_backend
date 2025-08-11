from app.database import SessionLocal
from app.schemas.property_schema import PropertyCreate
from app.schemas.property_owner_schema import PropertyOwnerCreate
from app.services import property_service, property_owner_service


def seed_properties():
    properties = [
        {
            "manager_id": 3,
            "title": "Beautiful 3-Bedroom House",
            "description": "Spacious family home with modern amenities, large backyard, and garage.",
            "price": 350000.00,
            "location": "123 Oak Street, Springfield, IL",
            "status": "available",
            "type": "house",
            "image_name": "property_1.jpg",
            "image_url": "/uploads/properties/property_1.jpg",
            "owners": [
                {
                    "owner_id": 5,
                    "ownership_start": "2025-08-11",
                }
            ],
        },
        {
            "manager_id": 3,
            "title": "Modern Downtown Apartment",
            "description": "Luxury 2-bedroom apartment in the heart of downtown.",
            "price": 2500.00,
            "location": "456 Main Avenue, Downtown, NY",
            "status": "available",
            "type": "apartment",
            "image_name": "property_2.jpg",
            "image_url": "/uploads/properties/property_2.jpg",
            "owners": [
                {
                    "owner_id": 5,
                    "ownership_start": "2025-08-11",
                }
            ],
        },
        {
            "manager_id": 3,
            "title": "Premium Office Space",
            "description": "Professional office space with modern facilities, conference rooms, and parking.",
            "price": 5000.00,
            "location": "789 Business District, Chicago, IL",
            "status": "available",
            "type": "office",
            "image_name": "property_3.jpg",
            "image_url": "/uploads/properties/property_3.jpg",
            "owners": [
                {
                    "owner_id": 5,
                    "ownership_start": "2025-08-11",
                }
            ],
        },
        {
            "manager_id": 2,
            "title": "Luxury Villa with Ocean View",
            "description": "Exclusive villa with stunning ocean views, private pool, and premium finishes.",
            "price": 1200000.00,
            "location": "321 Coastal Drive, Malibu, CA",
            "status": "available",
            "type": "villa",
            "image_name": "property_4.jpg",
            "image_url": "/uploads/properties/property_4.jpg",
            "owners": [
                {
                    "owner_id": 5,
                    "ownership_start": "2025-08-11",
                }
            ],
        },
        {
            "manager_id": 2,
            "title": "Prime Development Land",
            "description": "Large plot of land zoned for residential development. Utilities available at street.",
            "price": 150000.00,
            "location": "555 Development Road, Austin, TX",
            "status": "available",
            "type": "land",
            "image_name": "property_5.jpg",
            "image_url": "/uploads/properties/property_5.jpg",
            "owners": [
                {
                    "owner_id": 5,
                    "ownership_start": "2025-08-11",
                }
            ],
        },
    ]

    print("---> Seeding properties, please wait... <---")

    for prop in properties:
        newProperty = property_service.create_property(
            db=SessionLocal(),
            payload=PropertyCreate(
                manager_id=prop["manager_id"],
                title=prop["title"],
                description=prop["description"],
                price=prop["price"],
                location=prop["location"],
                status=prop["status"],
                type=prop["type"],
                image_name=prop["image_name"],
                image_url=prop["image_url"],
            ),
        )

        for owner in prop["owners"]:
            property_owner_service.create_owner(
                db=SessionLocal(),
                payload=PropertyOwnerCreate(
                    property_id=newProperty.id,
                    owner_id=owner["owner_id"],
                    ownership_start=owner["ownership_start"],
                ),
            )

    print("---> Seeding properties completed. <---")
