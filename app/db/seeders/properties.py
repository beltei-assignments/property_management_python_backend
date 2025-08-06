from app.database import SessionLocal
from app.schemas.property_schema import PropertyCreate
from app.services import property_service

def seed_properties():
    properties = [
        {
            "manager_id": 1,
            "title": "Beautiful 3-Bedroom House",
            "description": "Spacious family home with modern amenities, large backyard, and garage.",
            "price": 350000.00,
            "location": "123 Oak Street, Springfield, IL",
            "status": "available",
            "type": "house"
        },
        {
            "manager_id": 2,
            "title": "Modern Downtown Apartment",
            "description": "Luxury 2-bedroom apartment in the heart of downtown.",
            "price": 2500.00,
            "location": "456 Main Avenue, Downtown, NY",
            "status": "available",
            "type": "apartment"
        },
        {
            "manager_id": 3,
            "title": "Premium Office Space",
            "description": "Professional office space with modern facilities, conference rooms, and parking.",
            "price": 5000.00,
            "location": "789 Business District, Chicago, IL",
            "status": "available",
            "type": "office"
        },
        {
            "manager_id": 4,
            "title": "Luxury Villa with Ocean View",
            "description": "Exclusive villa with stunning ocean views, private pool, and premium finishes.",
            "price": 1200000.00,
            "location": "321 Coastal Drive, Malibu, CA",
            "status": "available",
            "type": "villa"
        },
        {
            "manager_id": 5,
            "title": "Prime Development Land",
            "description": "Large plot of land zoned for residential development. Utilities available at street.",
            "price": 150000.00,
            "location": "555 Development Road, Austin, TX",
            "status": "available",
            "type": "land"
        }
    ]

    for prop in properties:
        property_service.create_property(
            db=SessionLocal(),
            payload=PropertyCreate(
                manager_id=prop["manager_id"],
                title=prop["title"],
                description=prop["description"],
                price=prop["price"],
                location=prop["location"],
                status=prop["status"],
                type=prop["type"]
            )
        )
