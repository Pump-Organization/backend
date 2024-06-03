from services.attendee_service import AttendeeService
from services.service import Service
from tests.mocks.models import MockAttendee, MockUser

class MockAttendeeService(AttendeeService):
    def __init__(self) -> None:
        super().__init__()

    def create_attendee(self, data):
        return Service.ServiceResponse(status_code=200, data=MockAttendee(1, 1, 1, "guest", "pending"))
    
    def get_attendee(self, attendee_id):
        return Service.ServiceResponse(status_code=200, data=MockAttendee(1, 1, 1, "guest", "pending"))
    
    def list_workout_attendees(self, workout_id):
        return Service.ServiceResponse(status_code=200, data=[MockUser("John Doe", "john.doe@example.com", "johndoe", "https://example.com/johndoe.jpg")])
    
    def accept_workout(self, workout_id, user_id):
        return Service.ServiceResponse(status_code=200, data=MockAttendee(1, 1, 1, "guest", "accepted"))
    
    def delete_attendee(self, workout_id, user_id):
        return Service.ServiceResponse(status_code=204)
    