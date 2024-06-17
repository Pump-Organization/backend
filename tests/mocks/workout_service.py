from services.workout_service import WorkoutService
from services.service import Service
from tests.mocks.models import MockWorkout

class MockWorkoutService(WorkoutService):
    def __init__(self) -> None:
        super().__init__()

    def create_workout(self, data):
        return Service.ServiceResponse(status_code=200, data=MockWorkout("Morning Run", "Morning run around the park", "run"))

    def get_workout(self, workout_id):
        return Service.ServiceResponse(status_code=200, data=MockWorkout("Morning Run", "Morning run around the park", "run"))

    def update_workout(self, workout_id, data):
        return Service.ServiceResponse(status_code=200, data=MockWorkout("Morning Jog", "Morning run around the park", "run"))

    def delete_workout(self, workout_id):
        return Service.ServiceResponse(status_code=204)
    
    def get_upcoming_workouts(self, user_id, date, status="accepted", page=1):
        return Service.ServiceResponse(status_code=200, data=[{"title": "Morning Run", 
                                                               "description": "Morning run around the park", 
                                                               "workout_type": "run"}])
