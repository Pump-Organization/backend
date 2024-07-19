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
            workout_type = data.get('workout_type'),
            workout_pic = data.get('workout_pic'),
            location = data.get('location'),
            city = data.get('city'),
            datetime = parsed_datetime
        )
        workout_response = self.add_data(new_workout, False)
        if workout_response.status_code == 200:
            self.session.flush()
            organizer = Attendee(
                workout_id = new_workout.id,
                user_id = data.get('organizer_id'),
                attendee_type = "organizer",
                status = "accepted"
            )
            attendee_response = self.add_data(organizer)
            if attendee_response.status_code != 200:
                return attendee_response
            for invitee_id in data.get('invitees', []):
                guest = Attendee(
                    workout_id = new_workout.id,
                    user_id = invitee_id,
                    attendee_type = "guest",
                    status = "pending"
                )
                attendee_response = self.add_data(guest)

        return workout_response
    
    def get_workout(self, workout_id):
        return self.get_data(workout_id)
    
    def update_workout(self, workout_id, data):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        try:
            workout = self.model.query.get(workout_id)
            if workout:
                for key, value in data.items():
                    setattr(workout, key, value)
                self.session.commit()
                return self.ServiceResponse(status_code=200, data=workout)
            else:
                raise NotFoundError
        except Exception as e:
            return self.handle_error(e)
    
    def delete_workout(self, workout_id):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        try:
            self.session.query(Workout).filter(Workout.id==workout_id).delete()
            self.session.commit()
            return self.ServiceResponse(status_code=204)
        except Exception as e:
            return self.handle_error(e)
    
    def get_top_workout_types(self, user_id):
        subquery = (
            self.session.query(Workout.workout_type, func.count(Workout.workout_type).label('count'))
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(Attendee.user_id == user_id)
            .where(Workout.datetime < datetime.now())
            .group_by(Workout.workout_type)
            .subquery()
        )

        top_event_types = (
            self.session.query(subquery.c.workout_type, subquery.c.count)
            .order_by(subquery.c.count.desc())
            .limit(3)
            .all()
        )

        result_dict = {workout_type: count for workout_type, count in top_event_types}

        return self.ServiceResponse(status_code=200, data=result_dict)
        
    def get_upcoming_workouts(self, user_id, date, status="accepted", page=1):
        workouts = self.session.query(Workout).join(Attendee, Attendee.workout_id == Workout.id
        ).filter(Attendee.user_id == user_id
        ).filter(Attendee.status == status
        ).filter(Workout.datetime >= date, Workout.datetime
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
        return self.ServiceResponse(status_code=200, data=results)
    
    def get_organizer_id(self, workout_id):
        organizer = self.session.query(Attendee).filter(
            Attendee.workout_id == workout_id,
            Attendee.attendee_type == AttendeeTypeEnum.organizer
        ).first()
        return organizer.user_id if organizer else None
