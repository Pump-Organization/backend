from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.custom_user_exercise_service import CustomUserExerciseService


class CustomExercisesView(FlaskView):
    route_base = "custom_exercises"

    @route("", methods=["POST"])
    @token_required
    def create_custom_exercise(self):
        request_data = request.get_json()
        service_data = CustomUserExerciseService().create_custom_exercise(request_data)
        return service_data, 201
