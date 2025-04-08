from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from middleware.with_blocked_users_context import with_blocked_users_context
from services.user_service import UserService


class SearchView(FlaskView):
    route_base = "search"

    @route("", methods=["GET"])
    @token_required
    @with_blocked_users_context
    def search_users(self):
        search_query = request.args.get("q", "")
        page = request.args.get("page", 1, type=int)
        service_data = UserService().search_users(search_query, page)
        return [
            serialize_search_result(user, is_following, follow_status)
            for user, is_following, follow_status in service_data
        ], 200


def serialize_search_result(user, is_following, follow_status):
    ret = user.to_quickview()
    ret["is_following"] = is_following
    ret["follow_status"] = follow_status

    return ret
