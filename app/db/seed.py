from app.database import SessionLocal
from sqlalchemy import text
from app.models.user_model import User
from app.models.role_model import Role
from app.models.user_has_role_model import UserHasRole
from app.models.property_model import Property
from app.db.seeders.roles import seed_roles
from app.db.seeders.users import seed_users
from app.db.seeders.properties import seed_properties
import os
from app.database import Base, engine
from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func


def migrate_image_fields():
    """Add image_name and image_url columns to properties table if they don't exist"""
    print("---> Checking and adding image fields to properties table... <---")

    db = SessionLocal()
    try:
        # Check if image_name column exists
        result = db.execute(
            text(
                """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'properties' 
            AND COLUMN_NAME = 'image_name'
        """
            )
        )

        if not result.fetchone():
            print("Adding image_name column...")
            db.execute(
                text("ALTER TABLE properties ADD COLUMN image_name VARCHAR(255)")
            )
            print("✅ image_name column added successfully")
        else:
            print("✅ image_name column already exists")

        # Check if image_url column exists
        result = db.execute(
            text(
                """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'properties' 
            AND COLUMN_NAME = 'image_url'
        """
            )
        )

        if not result.fetchone():
            print("Adding image_url column...")
            db.execute(text("ALTER TABLE properties ADD COLUMN image_url VARCHAR(500)"))
            print("✅ image_url column added successfully")
        else:
            print("✅ image_url column already exists")

        db.commit()
        print("---> Image fields migration completed. <---")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
        raise e
    finally:
        db.close()


def seed():
    # Clean all tables before seeding (this also creates tables if needed)
    clean_all_tables()

    # Now run migration to add image fields (tables exist at this point)
    migrate_image_fields()

    print("---> Seeding roles, users, and properties, please wait... <---")
    seed_roles()
    seed_users()
    seed_properties()
    print("---> Seeding completed. <---")


def clean_all_tables():
    print("---> Cleaning all tables, please wait... <---")

    db = SessionLocal()
    try:
        # For many-to-many association tables, use execute
        # Delete in correct order to avoid foreign key constraint violations
        db.execute(UserHasRole.delete())
        if os.getenv("DB_CREATE_ALL_TABLE") == "true":
            Base.metadata.create_all(bind=engine)

        # Delete in order: child tables first, then parent tables
        db.query(Property).delete()  # Delete all properties first
        db.execute(text("DELETE FROM user_has_roles"))  # Delete user-role associations
        db.query(User).delete()  # Delete users
        db.query(Role).delete()  # Delete roles
        db.commit()

        # Reset auto-increment counters
        db.execute(text("ALTER TABLE users AUTO_INCREMENT = 1;"))
        db.execute(text("ALTER TABLE roles AUTO_INCREMENT = 1;"))
        db.execute(text("ALTER TABLE properties AUTO_INCREMENT = 1;"))
        db.commit()
    finally:
        db.close()

    print("---> Cleaning all tables completed. <---")


if __name__ == "__main__":
    seed()
