import json
from db.db import DbSession
from db.models import CustomUserExercise
from pathlib import Path
from settings import SYSTEM_USER_ID
from utils.create_system_user import create_system_user


def create_system_user_and_exercises():
    # create the system user
    create_system_user()

    # create the default exercises
    add_default_exercises()


def add_default_exercises():
    # create the system user exercises
    with Path("constants/default_exercises.json").open("r") as f:
        default_exercises = json.load(f)

    with DbSession() as session:
        for exercise in default_exercises:
            # skip if the exercise already exists
            if (
                session.query(CustomUserExercise)
                .filter_by(
                    name=exercise["name"],
                )
                .first()
            ):
                continue

            custom_exercise = CustomUserExercise(
                user_id=SYSTEM_USER_ID,
                name=exercise["name"],
                equipment=exercise["equipment"],
                muscle_group=exercise["muscle_group"],
                metric_type=exercise["metric_type"],
            )
            session.add(custom_exercise)
        session.commit()


if __name__ == "__main__":
    create_system_user_and_exercises()
    print("System user and exercises created successfully.")
