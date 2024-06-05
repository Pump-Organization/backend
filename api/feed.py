from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.profile_service import ProfileService

class FeedView(FlaskView):
    route_base = 'feed'

    @route('', methods=['GET'])
    @token_required
    def get_feed(self):
        page = request.args.get('page', 1, type=int)
        service_response = ProfileService().get_feed(page)
        return [workout.to_json() for workout in service_response.data], service_response.status_code
    