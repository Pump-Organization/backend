from datetime import datetime
from db.models import Attendee, AttendeeStatusEnum, Workout
from services.user_service import UserService
from services.friendship_service import FriendshipService
from services.workout_service import WorkoutService
from services.attendee_service import AttendeeService
from services.service import Service
import constants


class ProfileService(Service):
    def get_profile(self, user_id):
        user_response = UserService().get_user(user_id)
        if user_response.status_code != 200:
            return user_response
        friendship_response = FriendshipService().get_frienship_count(user_id)
        workout_counts_response = WorkoutService().get_top_workout_types(user_id)
        response_data = {
            'id': user_response.data.id,
            'username': user_response.data.username,
            'profile_pic': user_response.data.profile_pic,
            'location': user_response.data.location,
            'email': user_response.data.email,
            'bio': user_response.data.bio,
            'num_friends': friendship_response.data,
            'workout_counts': workout_counts_response.data
        }

        return self.ServiceResponse(status_code=200, data=response_data)
    
    def get_profile_workouts(self, user_id, page):
        per_page = constants.POSTS_PER_PAGE
        now = datetime.now()
        offset = (page - 1) * per_page

        past_workouts = self.session.query(Workout).join(Attendee).filter(
            Attendee.user_id == user_id,
            Attendee.status == AttendeeStatusEnum.accepted,
            Workout.datetime < now
        ).order_by(Workout.datetime.desc()).offset(offset).limit(per_page).all()

        response_data = [workout.to_json() for workout in past_workouts]
        
        return self.ServiceResponse(data=response_data, status_code=200)
