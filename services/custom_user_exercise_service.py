import json
from constants.error_constants import ForbiddenError, NotFoundError
from db.models.custom_user_exercise import CustomUserExercise
from flask import g
from pathlib import Path
from services.service import Service


class CustomUserExerciseService(Service):
    def __init__(self) -> None:
        super().__init__(CustomUserExercise)

    def create_custom_exercise(self, data):
        custom_exercise = CustomUserExercise(
            user_id=g.user_id,
            name=data.get("name"),
            equipment=data.get("equipment"),
            muscle_group=data.get("muscle_group"),
            metric_type=data.get("metric_type"),
        )
        custom_exercise = self.add_data(custom_exercise)

        return custom_exercise.to_json()

    def update_custom_exercise(self, data):
        custom_exercise = (
            self.session.query(CustomUserExercise)
            .filter(CustomUserExercise.id == data.get("id"))
            .first()
        )
        if not custom_exercise:
            raise NotFoundError

        if g.user_id != custom_exercise.user_id:
            raise ForbiddenError

        for key, value in data.items():
            setattr(custom_exercise, key, value)

        self.session.commit()

        return custom_exercise.to_json()

    def list_custom_exercises(self):
        custom_exercises = (
            self.session.query(CustomUserExercise)
            .filter(CustomUserExercise.user_id == g.user_id)
            .all()
        )
        return [exercise.to_json() for exercise in custom_exercises]

    def delete_custom_exercise(self, custom_exercise_id):
        custom_exercise = (
            self.session.query(CustomUserExercise)
            .filter(CustomUserExercise.id == custom_exercise_id)
            .first()
        )
        if not custom_exercise:
            return

        if g.user_id != custom_exercise.user_id:
            raise ForbiddenError

        self.session.delete(custom_exercise)
        self.session.commit()

    def get_all_exercises(self):
        custom_exercises = self.list_custom_exercises()
        with Path("constants/default_exercises.json").open("r") as f:
            default_exercises = json.load(f)

        return default_exercises + custom_exercises
