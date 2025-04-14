from db.models.custom_user_exercise import CustomUserExercise
from flask import g
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
