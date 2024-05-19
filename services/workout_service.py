from db.models.workout import Workout
from db.models.attendee import Attendee
from services.service import Service
from datetime import datetime, timedelta
from sqlalchemy import func
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
        return self.update_data(id=workout_id, updated_data=data)
    
    def delete_workout(self, workout_id):
        return self.delete_data(workout_id)
    
    def get_top_workout_types(self, user_id):
        subquery = (
            self.session.query(Workout.workout_type, func.count(Workout.workout_type).label('count'))
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(Attendee.user_id == user_id)
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
        
    def get_upcoming_workouts(self, user_id, date, status="accepted"):
        workouts = (
            self.session.query(Workout)
            .join(Attendee, Attendee.workout_id == Workout.id)
            .filter(Attendee.user_id == user_id)
            .filter(Attendee.status == status)
            .filter(Workout.datetime >= date, Workout.datetime < date + timedelta(days=1))
            .all()
        )

        return self.ServiceResponse(status_code=200, data=workouts)
    