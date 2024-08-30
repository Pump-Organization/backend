from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.profile_service import ProfileService

class ProfilesView(FlaskView):
    route_base = 'profiles'
    
    @route('/<user_id>', methods=['GET'])
    @token_required
    def get_profile(self, user_id):
        service_data = ProfileService().get_profile(user_id)
        return service_data, 200
    
    @route('/<user_id>/workouts', methods=['GET'])
    @token_required
    def get_profile_workouts(self, user_id):
        page = request.args.get('page', 1, int)
        service_data = ProfileService().get_profile_workouts(user_id, page)
        return service_data, 200
