from services.profile_service import ProfileService
from services.service import Service
from tests.mocks.models import MockWorkout

class MockProfileService(ProfileService):
    def __init__(self) -> None:
        super().__init__()

    def get_feed(self):
        return Service.ServiceResponse(status_code=200, data=[MockWorkout("Morning Run", "Morning run around the park", "run")])
