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

    @route("/<custom_exercise_id>", methods=["PATCH"])
    @token_required
    def update_custom_exercise(self, custom_exercise_id):
        request_data = request.get_json()
        request_data["id"] = custom_exercise_id
        service_data = CustomUserExerciseService().update_custom_exercise(request_data)
        return service_data, 200

    @route("/<custom_exercise_id>", methods=["DELETE"])
    @token_required
    def delete_custom_exercise(self, custom_exercise_id):
        CustomUserExerciseService().delete_custom_exercise(custom_exercise_id)
        return "", 204


class ExercisesView(FlaskView):
    route_base = "exercises"

    @route("", methods=["GET"])
    @token_required
    def list_exercises(self):
        service_data = CustomUserExerciseService().get_all_exercises()
        return service_data, 200
