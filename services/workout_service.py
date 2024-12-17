import settings
from db.models.workout import Workout, WorkoutStatusEnum
from db.models.attendee import Attendee, AttendeeStatusEnum, AttendeeTypeEnum
from services.service import Service
from services.attendee_service import AttendeeService
from constants.error_constants import ForbiddenError, NotFoundError
from datetime import datetime
from flask import g
from sqlalchemy.orm import joinedload


class WorkoutService(Service):
    def __init__(self) -> None:
        super().__init__(Workout)

    def create_workout(self, data):
        parsed_datetime = datetime.strptime(data['datetime'], settings.DATETIME_REPRESENTATION)
        parsed_endtime = datetime.strptime(data['endtime'], settings.DATETIME_REPRESENTATION)

        new_workout = Workout(
            title=data.get('title'),
            description=data.get('description'),
            workout_pic=data.get('workout_pic'),
            location=data.get('location'),
            city=data.get('city'),
            datetime=parsed_datetime,
            endtime=parsed_endtime,
        )
        workout_data = self.add_data(new_workout, False)
        self.session.flush()
        organizer_data = {
            "workout_id": new_workout.id,
            "user_id": data.get('organizer_id'),
            "attendee_type": AttendeeTypeEnum.organizer,
        }

        AttendeeService().create_attendee(data=organizer_data, status=AttendeeStatusEnum.accepted, organizer_id=data.get('organizer_id'))
        for invitee_id in data.get('invitees', []):
            guest_data = {
                "workout_id": new_workout.id,
                "user_id": invitee_id,
                "attendee_type": AttendeeTypeEnum.guest,
            }
            AttendeeService().create_attendee(data=guest_data, status=AttendeeStatusEnum.pending, organizer_id=data.get('organizer_id'))

        return workout_data

    def get_workout(self, workout_id):
        return self.get_data(workout_id)

    def update_workout(self, workout_id, data):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        workout = self.session.get(self.model, workout_id)
        if workout:
            for key, value in data.items():
                if key == "datetime" or key == "endtime":
                    value = datetime.strptime(value, settings.DATETIME_REPRESENTATION)
                setattr(workout, key, value)
            self.session.commit()
            return workout
        else:
            raise NotFoundError

    def delete_workout(self, workout_id):
        if g.user_id != self.get_organizer_id(workout_id):
            raise ForbiddenError
        self.session.query(Workout).filter(Workout.id == workout_id).delete()
        self.session.commit()
        return

    def get_num_workouts(self, user_id):
        num_workouts = self.session.query(Attendee.workout_id).\
            filter(Attendee.user_id == user_id,
                   Attendee.status == AttendeeStatusEnum.accepted).count()
        return num_workouts

    def get_pending_workouts(self, page=1):
        workouts = self.session.query(Workout).join(Attendee, Attendee.workout_id == Workout.id)\
            .filter(Workout.endtime < datetime.now())\
            .filter(Attendee.user_id == g.user_id)\
            .filter(Attendee.attendee_type == AttendeeTypeEnum.organizer)\
            .filter(Workout.status == WorkoutStatusEnum.pending)\
            .options(joinedload(Workout.attendees).joinedload(Attendee.user))\
            .limit(settings.WORKOUTS_PER_PAGE).offset((page - 1) * settings.WORKOUTS_PER_PAGE)

        results = []
        for workout in workouts:
            results.append(workout.to_json())
        return results

    def get_upcoming_workouts(self, user_id, date, status="accepted", page=1):
        workouts = self.session.query(Workout).join(Attendee, Attendee.workout_id == Workout.id)\
            .filter(Attendee.user_id == user_id)\
            .filter(Attendee.status == status)\
            .filter(Workout.datetime >= date)\
            .options(joinedload(Workout.attendees).joinedload(Attendee.user))\
            .limit(settings.WORKOUTS_PER_PAGE).offset((page - 1) * settings.WORKOUTS_PER_PAGE)

        results = []
        for workout in workouts:
            organizer = next(attendee.user for attendee in workout.attendees
                             if attendee.attendee_type == AttendeeTypeEnum.organizer)
            workout_json = workout.to_json()
            workout_json['organizer_username'] = organizer.username if organizer else None
            workout_json['organizer_pic'] = organizer.profile_pic if organizer else None
            workout_json['num_attendees'] = sum(1 for attendee in workout.attendees
                                                if attendee.status == AttendeeStatusEnum.accepted)
            results.append(workout_json)
        return results

    def get_organizer_id(self, workout_id):
        organizer = self.session.query(Attendee).filter(
            Attendee.workout_id == workout_id,
            Attendee.attendee_type == AttendeeTypeEnum.organizer
        ).first()
        return organizer.user_id if organizer else None

    def publish_workout(self, workout_id):
        return self.update_workout(workout_id, {"status": "published", "published_at": datetime.now()})  # noqa E501
