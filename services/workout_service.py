from db.models.workout import Workout
from db.models.attendee import Attendee, AttendeeStatusEnum, AttendeeTypeEnum
from services.service import Service
from constants.error_constants import ForbiddenError, NotFoundError
from constants import WORKOUTS_PER_PAGE
from datetime import datetime, timedelta
from flask import g
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import constants


class WorkoutService(Service):
    def __init__(self) -> None:
        super().__init__(Workout)

    def create_workout(self, data):
        parsed_datetime = datetime.strptime(data['datetime'], constants.DATETIME_REPRESENTATION)
        
        new_workout = Workout(
            title = data.get('title'),
            description = data.get('description'),
            workout_pic = data.get('workout_pic'),
            location = data.get('location'),
            city = data.get('city'),
            datetime = parsed_datetime
        )
        workout_data = self.add_data(new_workout, False)
        self.session.flush()
        organizer = Attendee(
            workout_id = new_workout.id,
            user_id = data.get('organizer_id'),
            attendee_type = "organizer",
            status = "accepted"
        )
        self.add_data(organizer)
        for invitee_id in data.get('invitees', []):
            guest = Attendee(
                workout_id = new_workout.id,
                user_id = invitee_id,
                attendee_type = "guest",
                status = "pending"
            )
            self.add_data(guest)

        return workout_data
    
    def get_workout(self, workout_id):
        return self.get_data(workout_id)
    
    def update_workout(self, workout_id, data):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        workout = self.model.query.get(workout_id)
        if workout:
            for key, value in data.items():
                setattr(workout, key, value)
            self.session.commit()
            return workout
        else:
            raise NotFoundError
    
    def delete_workout(self, workout_id):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        self.session.query(Workout).filter(Workout.id==workout_id).delete()
        self.session.commit()
        return
        
    def get_num_workouts(self, user_id):
        num_workouts = self.session.query(Attendee.workout_id).\
            filter(Attendee.user_id == user_id, Attendee.status == AttendeeStatusEnum.accepted).count()
        return num_workouts
        
    def get_upcoming_workouts(self, user_id, date, status="accepted", page=1):
        workouts = self.session.query(Workout).join(Attendee, Attendee.workout_id == Workout.id
        ).filter(Attendee.user_id == user_id
        ).filter(Attendee.status == status
        ).filter(Workout.datetime >= date
        ).options(
            joinedload(Workout.attendees).joinedload(Attendee.user)
        ).limit(WORKOUTS_PER_PAGE).offset((page - 1) * WORKOUTS_PER_PAGE)

        results = []
        for workout in workouts:
            organizer = next(attendee.user for attendee in workout.attendees if attendee.attendee_type == AttendeeTypeEnum.organizer)
            workout_json = workout.to_json()
            workout_json['organizer_username'] = organizer.username if organizer else None
            workout_json['num_attendees'] = sum(1 for attendee in workout.attendees if attendee.status == AttendeeStatusEnum.accepted)
            results.append(workout_json)
        return results
    
    def get_organizer_id(self, workout_id):
        organizer = self.session.query(Attendee).filter(
            Attendee.workout_id == workout_id,
            Attendee.attendee_type == AttendeeTypeEnum.organizer
        ).first()
        return organizer.user_id if organizer else None
