from app.database import SessionLocal
from app.schemas import user_schema as user_schema
from app.services import user_service as user_service


def seed_users():
    users = [
        {
            "email": "admin@example.com",
            "password": "123",
            "first_name": "Admin",
            "last_name": "User",
            "phone_number": "1234567890",
            "roles_ids": [1],
        },
        {
            "email": "sreyka@example.com",
            "password": "123",
            "first_name": "Sreyka",
            "last_name": "Thor",
            "phone_number": "1234567890",
            "roles_ids": [2],
        },
        {
            "email": "vanda@example.com",
            "password": "123",
            "first_name": "Vanda",
            "last_name": "Sophal",
            "phone_number": "1234567890",
            "roles_ids": [2],
        },
        {
            "email": "chetra@example.com",
            "password": "123",
            "first_name": "Chetra",
            "last_name": "Hong",
            "phone_number": "1234567890",
            "roles_ids": [3],
        },
        {
            "email": "nita@example.com",
            "password": "123",
            "first_name": "Nita",
            "last_name": "Sao",
            "phone_number": "1234567890",
            "roles_ids": [4],
        },
    ]

    print("---> Seeding users, please wait... <---")

    for user in users:
        user_service.create_user(
            db=SessionLocal(),
            userPayload=user_schema.UserCreate(
                email=user["email"],
                password=user["password"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                phone_number=user["phone_number"],
                roles_ids=user["roles_ids"],
            ),
        )

    print("---> Seeding users completed. <---")
