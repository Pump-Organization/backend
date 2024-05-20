from flask_classful import FlaskView, route
from flask import request
from decorators.token_required import token_required
from services.profile_service import ProfileService

class FeedView(FlaskView):
    route_base = 'feed'

    @route('', methods=['GET'])
    @token_required
    def get_feed(self):
        user_id = request.user_id
        service_response = ProfileService().get_feed(user_id)
        return [workout.to_json() for workout in service_response.data], service_response.status_code
    