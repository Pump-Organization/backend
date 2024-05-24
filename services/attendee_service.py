from flask import g
from db.models.attendee import Attendee, AttendeeStatusEnum, AttendeeTypeEnum
from constants.error_constants import ForbiddenError, NotFoundError
from services.service import Service


class AttendeeService(Service):
    def __init__(self) -> None:
        super().__init__(Attendee)

    def create_attendee(self, data):
        if g.user_id != self.get_workout_organizer(data.get('workout_id')):
            raise ForbiddenError
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
    
    def delete_attendee(self, workout_id, user_id):
        try:
            attendee = self.session.query(Attendee).filter(
                Attendee.workout_id == workout_id,
                Attendee.user_id == user_id
            ).first()
            if not attendee:
                return self.ServiceResponse(status_code=204)
            if g.user_id != attendee.user_id and g.user_id != self.get_workout_organizer(attendee.workout_id):
                raise ForbiddenError
            self.session.delete(attendee)
            self.session.commit()
            return self.ServiceResponse(status_code=204)
        except Exception as e:
            return self.handle_error(e)
    
    def get_workout_organizer(self, workout_id):
        organizer = self.session.query(Attendee).filter(
            Attendee.workout_id == workout_id,
            Attendee.attendee_type == AttendeeTypeEnum.organizer
        ).first()
        return organizer.user_id if organizer else None
    
    def accept_workout(self, workout_id, user_id):
        attendee = self.session.query(Attendee).filter(
            Attendee.workout_id == workout_id,
            Attendee.user_id == user_id
        ).first()

        attendee.status = AttendeeStatusEnum.accepted
        self.session.commit()
        return self.ServiceResponse(data=attendee, status_code=200)
