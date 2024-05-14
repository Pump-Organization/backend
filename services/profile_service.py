from services.user_service import UserService
from services.friendship_service import FriendshipService
from services.workout_service import WorkoutService
from services.service import Service


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
