from db.models.workout import Workout
from services.service import Service
from datetime import datetime


class WorkoutService(Service):
    def __init__(self) -> None:
        super().__init__(Workout)

    def create_workout(self, data):
        parsed_date = datetime.strptime(data.get('date'), '%m/%d/%y')
        parsed_time = datetime.strptime(data.get('time'), '%H:%M')
        
        new_workout = Workout(
            organizer_id = data.get('organizer_id'),
            title = data.get('title'),
            description = data.get('description'),
            workout_type = data.get('workout_type'),
            workout_pic = data.get('workout_pic'),
            date = parsed_date,
            time = parsed_time
        )
        return self.add_data(new_workout)
    
    def get_workout(self, workout_id):
        return self.get_data(workout_id)
    
    def update_workout(self, workout_id, data):
        return self.update_data(id=workout_id, updated_data=data)
    
    def delete_workout(self, workout_id):
        return self.delete_data(workout_id)
        