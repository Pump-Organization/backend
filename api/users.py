from flask_classful import FlaskView, route
from flask import g, request
from middleware.check_privacy import check_privacy
from middleware.token_required import token_required
from services.user_service import UserService


class UsersView(FlaskView):
    route_base = "users"

    @route("", methods=["POST"])
    def create_user(self):
        request_data = request.get_json()
        service_data = UserService().create_user(request_data)
        return service_data.to_json(), 200

    @route("/<user_id>", methods=["GET"])
    def get_user(self, user_id):
        service_data = UserService().get_user(user_id)
        return service_data.to_json(), 200

    @route("/<user_id>", methods=["PATCH"])
    @token_required
    def update_user(self, user_id):
        request_data = request.get_json()
        service_data = UserService().update_user(user_id, data=request_data)
        return service_data.to_json(), 200

    @route("/<user_id>", methods=["DELETE"])
    @token_required
    def delete_user(self, user_id):
        UserService().delete_user(user_id)
        return "", 204

    @route("/<user_id>/follow", methods=["POST"])
    @token_required
    def follow_user(self, user_id):
        service_data = UserService().follow_user(user_id)
        return service_data.to_json(), 200

    @route("/<user_id>/unfollow", methods=["POST"])
    @token_required
    def unfollow_user(self, user_id):
        UserService().delete_follower(g.user_id.hex, user_id)
        return "", 204

    @route("/<user_id>/follower", methods=["DELETE"])
    @token_required
    def remove_follower(self, user_id):
        UserService().delete_follower(user_id, g.user_id.hex)
        return "", 204

    @route("/<user_id>/follower", methods=["PUT"])
    @token_required
    def accept_follow_request(self, user_id):
        service_data = UserService().accept_follow_request(user_id)
        return service_data, 200

    @route("/<user_id>/followers", methods=["GET"])
    @token_required
    @check_privacy
    def get_followers(self, user_id):
        page = request.args.get("page", 1, int)
        service_data = UserService().get_followers(user_id, page)
        return [follower.to_quickview() for follower in service_data], 200

    @route("/follow_requests", methods=["GET"])
    @token_required
    def get_follow_requests(self):
        page = request.args.get("page", 1, int)
        service_data = UserService().get_follow_requests(page)
        return [follow_request.to_quickview() for follow_request in service_data], 200

    @route("/<user_id>/following", methods=["GET"])
    @token_required
    @check_privacy
    def get_followings(self, user_id):
        page = request.args.get("page", 1, int)
        service_data = UserService().get_followings(user_id, page)
        return [following.to_quickview() for following in service_data], 200

    @route("/blocks", methods=["GET"])
    @token_required
    def list_blocked_users(self):
        """
        get all blocks for the current user
        """
        page = request.args.get("page", 1, int)
        service_data = UserService().list_blocks(page)
        return service_data, 200

    @route("/<user_id>/block", methods=["POST"])
    @token_required
    def block_user(self, user_id):
        """
        block a user
        """
        service_data = UserService().block_user(user_id)
        return service_data, 200
