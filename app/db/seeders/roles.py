from app.database import SessionLocal
from app.models.role_model import Role


def seed_roles():
    db = SessionLocal()
    role = [
        {"name": "Admin", "value": "admin"},
        {"name": "Manager", "value": "manager"},
        {"name": "Buyer", "value": "buyer"},
        {"name": "Seller", "value": "seller"},
    ]
    try:
        for r in role:
            db.add(Role(**r))
        db.commit()
    finally:
        db.close()
