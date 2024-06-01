from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.user_service import UserService

class SearchView(FlaskView):
    route_base = 'search'

    @route('', methods=['GET'])
    @token_required
    def get_feed(self):
        search_query = request.args.get('q', "")
        page = request.args.get('page', 1, type=int)
        service_response = UserService().search_users(search_query, page)
        return [user.to_quickview() for user in service_response.data], service_response.status_code
    