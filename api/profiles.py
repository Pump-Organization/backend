from flask_classful import FlaskView, route
from flask import jsonify
from services.profile_service import ProfileService

class ProfilesView(FlaskView):
    route_base = 'profiles'
    
    @route('/<user_id>', methods=['GET'])
    def get_profile(self, user_id):
        service_response = ProfileService().get_profile(user_id)
        return jsonify(service_response.data), service_response.status_code
