from argon2 import PasswordHasher
from db.db import DbSession
from db.models import User
from random import choice
from string import ascii_letters, digits
from settings import SYSTEM_USER_ID


def create_system_user():
    with DbSession() as session:
        existing_user = session.get(User, SYSTEM_USER_ID)
        if existing_user:
            print("System user already exists.")
            return

        # Create a new system user
        system_user = User(
            id=SYSTEM_USER_ID,
            username="system",
            hashed_password=PasswordHasher().hash(choice(ascii_letters + digits) * 10),
            email="system@test.com",
        )

        # add the system user to the session and commit
        session.add(system_user)
        session.commit()
        print("System user created successfully.")
    return system_user
