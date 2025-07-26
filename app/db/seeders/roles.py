from app.database import SessionLocal
from app.models.role_model import Role


def seed_roles():
    db = SessionLocal()
    roles = [
        {"name": "Admin", "value": "admin"},
        {"name": "Manager", "value": "manager"},
        {"name": "Buyer", "value": "buyer"},
        {"name": "Seller", "value": "seller"},
    ]
    try:
        for role in roles:
            db.add(Role(**role))
        db.commit()
    finally:
        db.close()
