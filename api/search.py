from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.user_service import UserService

class SearchView(FlaskView):
    route_base = 'search'

    @route('', methods=['GET'])
    @token_required
    def search_users(self):
        search_query = request.args.get('q', "")
        page = request.args.get('page', 1, type=int)
        service_response = UserService().search_users(search_query, page)
        return [serialize_search_result(user, friendship_status, friendship_id) for user, friendship_status, friendship_id in service_response.data], service_response.status_code
    


def serialize_search_result(user, friendship_status, friendship_id):
    ret = user.to_quickview()
    if friendship_status is None:
        friendship_status = "not_friends"
    ret['friendship_status'] = friendship_status
    ret['friendship_id'] = friendship_id
    return ret

    