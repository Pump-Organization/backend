from flask import g
from db.models.attendee import Attendee
from constants.error_constants import ForbiddenError, NotFoundError
from services.service import Service


class AttendeeService(Service):
    def __init__(self) -> None:
        super().__init__(Attendee)

    def create_attendee(self, data):
        # TODO: Should only be allowed by workout organizer
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
        try:
            attendee = self.model.query.get(attendee_id)
            if not attendee:
                raise NotFoundError
            if attendee.user_id != g.user_id:
                raise ForbiddenError
            for key, value in data.items():
                setattr(attendee, key, value)
            self.session.commit()
            return self.ServiceResponse(status_code=200, data=attendee)
        except Exception as e:
            return self.handle_error(e)
    
    def delete_attendee(self, attendee_id):
        # TODO: both the attendee user and the workout organizer should be allowed to do this
        return self.delete_data(attendee_id)