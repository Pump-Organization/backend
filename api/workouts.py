from datetime import datetime
from flask_classful import FlaskView, route
from flask import g, request
from decorators.token_required import token_required
from services.workout_service import WorkoutService


class WorkoutsView(FlaskView):
    route_base = 'workouts'

    @route('upcoming', methods=['GET'])
    @token_required
    def get_upcoming(self):
        date = datetime.strptime(request.args.get('date'), '%m/%d/%y')
        user_id = g.user_id
        service_response = WorkoutService().get_upcoming_workouts(user_id, date)
        return [workout.to_json() for workout in service_response.data], service_response.status_code
    
    @route('invites', methods=['GET'])
    @token_required
    def get_invites(self):
        date = datetime.strptime(request.args.get('date'), '%m/%d/%y')
        user_id = g.user_id
        service_response = WorkoutService().get_upcoming_workouts(user_id, date, "pending")
        return [workout.to_json() for workout in service_response.data], service_response.status_code

    @route('', methods=['POST'])
    @token_required
    def create_workout(self):
        request_data = request.get_json()
        request_data['organizer_id'] = g.user_id
        service_response = WorkoutService().create_workout(request_data)
        return service_response.data.to_json(), service_response.status_code
    
    @route('/<workout_id>', methods=['GET'])
    def get_workout(self, workout_id):
        service_response = WorkoutService().get_workout(workout_id)
        return service_response.data.to_json(), service_response.status_code

    @route('/<workout_id>', methods=['PATCH'])
    @token_required
    def update_workout(self, workout_id):
        request_data = request.get_json()
        service_response = WorkoutService().update_workout(workout_id, data=request_data)
        return service_response.data.to_json(), service_response.status_code

    @route('/<workout_id>', methods=['DELETE'])
    def delete_workout(self, workout_id):
        service_response = WorkoutService().delete_workout(workout_id)
        return service_response.data, service_response.status_code
