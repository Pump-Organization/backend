from flask_classful import FlaskView, route
from flask import jsonify, request
from services.workout_service import WorkoutService

class WorkoutsView(FlaskView):
    route_base = 'workouts'

    @route('', methods=['GET'])
    def test(self):
        return "Hello World", 200
    
    @route('', methods=['POST'])
    def create_workout(self):
        request_data = request.get_json()
        service_response = WorkoutService().create_workout(request_data)
        return jsonify(service_response.data), service_response.status_code
    
    @route('/<workout_id>', methods=['GET'])
    def get_workout(self, workout_id):
        service_response = WorkoutService().get_workout(workout_id)
        return jsonify(service_response.data), service_response.status_code

    @route('/<workout_id>', methods=['PATCH'])
    def update_workout(self, workout_id):
        request_data = request.get_json()
        service_response = WorkoutService().update_workout(workout_id, data=request_data)
        return jsonify(service_response.data), service_response.status_code

    @route('/<workout_id>', methods=['DELETE'])
    def delete_workout(self, workout_id):
        service_response = WorkoutService().delete_workout(workout_id)
        return jsonify(service_response.data), service_response.status_code
