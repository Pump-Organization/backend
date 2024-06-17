from services.profile_service import ProfileService
from services.service import Service
from tests.mocks.models import MockWorkout, MockProfile


class MockProfileService(ProfileService):
    def __init__(self) -> None:
        super().__init__()

    def get_feed(self, page=1):
        return Service.ServiceResponse(status_code=200, data=[{"title": "Morning Run",
                                                               "description": "Morning run around the park",
                                                               "workout_type": "run"}])
    
    def get_profile(self, user_id):
        return Service.ServiceResponse(status_code=200, data={
            "name": "John Doe", 
            "email": "john.doe@example.com", 
            "username": "johndoe", 
            "profile_pic": "https://example.com/johndoe.jpg", 
            "num_friends": 2, 
            "workout_counts": {"run": 2, "lift": 1, "bike": 1}
            })
    
    def get_profile_workouts(self, user_id, page):
        return Service.ServiceResponse(status_code=200, data=[{"title": "Morning Run", 
                                                               "description": "Morning run around the park", 
                                                               "workout_type": "run"}])
    