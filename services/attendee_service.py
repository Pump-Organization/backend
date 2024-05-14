from services.service import Service
from db.models.attendee import Attendee


class AttendeeService(Service):
    def __init__(self) -> None:
        super().__init__(Attendee)

    def create_attendee(self, data):
        attendee = Attendee(
            user_id = data.get('user_id'),
            workout_id = data.get('workout_id'),
            attendee_type = data.get('attendee_type', 'guest'),
            status = "pending"
        )
        return self.add_data(attendee)
    
    def get_attendee(self, attendee_id):
        return self.get_data(attendee_id)
    
    def update_attendee(self, attendee_id, data):
        return self.update_data(id=attendee_id, updated_data=data)
    
    def delete_attendee(self, attendee_id):
        return self.delete_data(attendee_id)