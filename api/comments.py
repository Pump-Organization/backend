from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from middleware.with_blocked_users_context import with_blocked_users_context
from services.comment_service import CommentService
from utils.comment_utils import get_num_comments


class CommentsView(FlaskView):
    route_base = "comments"

    @route("", methods=["POST"])
    @token_required
    @with_blocked_users_context
    def create_comment(self):
        request_data = request.get_json()
        service_data = CommentService().create_comment(request_data)
        return service_data, 200

    @route("/<workout_id>", methods=["GET"])
    @token_required
    @with_blocked_users_context
    def get_comments(self, workout_id):
        page = request.args.get("page", 1, int)
        service_data = CommentService().get_comments(workout_id, page)
        return service_data, 200

    @route("/<comment_id>", methods=["DELETE"])
    @token_required
    def delete_comment(self, comment_id):
        CommentService().delete_comment(comment_id)
        return "", 204

    @route("/<workout_id>/num_comments", methods=["GET"])
    @token_required
    def get_num_comments(self, workout_id):
        service_data = get_num_comments(workout_id)
        return {"num_comments": service_data}, 200
