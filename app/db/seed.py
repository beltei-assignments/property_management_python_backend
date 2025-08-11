from app.database import SessionLocal
from sqlalchemy import text
from app.models.user_model import User
from app.models.role_model import Role
from app.models.user_has_role_model import UserHasRole
from app.models.property_model import Property
from app.models.property_owner_model import PropertyOwner
from app.db.seeders.roles import seed_roles
from app.db.seeders.users import seed_users
from app.db.seeders.properties import seed_properties


def seed():
    clean_all_tables()

    seed_roles()
    seed_users()
    seed_properties()


def clean_all_tables():
    print("---> Cleaning all tables, please wait... <---")

    db = SessionLocal()
    try:
        db.query(PropertyOwner).delete()
        db.query(Property).delete()
        db.execute(UserHasRole.delete())
        db.query(User).delete()
        db.query(Role).delete()
        db.commit()

        # Reset auto-increment counters
        db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1;"))
        db.execute(text("ALTER TABLE roles AUTO_INCREMENT = 1;"))
        db.execute(text("ALTER TABLE properties AUTO_INCREMENT = 1;"))
        db.execute(text("ALTER TABLE property_owners AUTO_INCREMENT = 1;"))
        db.commit()
    finally:
        db.close()

    print("---> Cleaning all tables completed. <---")


if __name__ == "__main__":
    seed()
