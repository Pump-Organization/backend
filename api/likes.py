from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.like_service import LikeService
from utils.like_utils import get_num_likes


class LikesView(FlaskView):
    route_base = 'likes'

    @route('', methods=['POST'])
    @token_required
    def create_like(self):
        request_data = request.get_json()
        service_data = LikeService().create_like(request_data)
        return service_data.to_json(), 200

    @route('/<workout_id>', methods=['GET'])
    @token_required
    def get_likes(self, workout_id):
        page = request.args.get('page', 1, int)
        service_data = LikeService().get_likes(workout_id, page)
        return [like.to_json() for like in service_data], 200

    @route('/<workout_id>', methods=['DELETE'])
    @token_required
    def delete_like(self, workout_id):
        LikeService().delete_like(workout_id)
        return '', 204

    @route('/<workout_id>/num_likes', methods=['GET'])
    @token_required
    def get_num_likes(self, workout_id):
        service_data = get_num_likes(workout_id)
        return {"num_likes": service_data}, 200
