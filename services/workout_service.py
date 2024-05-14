from db.models.workout import Workout
from db.models.attendee import Attendee
from services.service import Service
from datetime import datetime


class WorkoutService(Service):
    def __init__(self) -> None:
        super().__init__(Workout)

    def create_workout(self, data):
        parsed_date = datetime.strptime(data.get('date'), '%m/%d/%y')
        parsed_time = datetime.strptime(data.get('time'), '%H:%M')
        
        new_workout = Workout(
            title = data.get('title'),
            description = data.get('description'),
            workout_type = data.get('workout_type'),
            workout_pic = data.get('workout_pic'),
            date = parsed_date,
            time = parsed_time
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

        return workout_response
    
    def get_workout(self, workout_id):
        return self.get_data(workout_id)
    
    def update_workout(self, workout_id, data):
        return self.update_data(id=workout_id, updated_data=data)
    
    def delete_workout(self, workout_id):
        return self.delete_data(workout_id)
        