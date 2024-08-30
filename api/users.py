from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.user_service import UserService
from services.friendship_service import FriendshipService

class UsersView(FlaskView):
    route_base = 'users'
    
    @route('', methods=['POST'])
    def create_user(self):
        request_data = request.get_json()
        service_data = UserService().create_user(request_data)
        return service_data.to_json(), 200
    
    @route('/<user_id>', methods=['GET'])
    def get_user(self, user_id):
        service_data = UserService().get_user(user_id)
        return service_data.to_json(), 200

    @route('/<user_id>', methods=['PATCH'])
    @token_required
    def update_user(self, user_id):
        request_data = request.get_json()
        service_data = UserService().update_user(user_id, data=request_data)
        return service_data.to_json(), 200

    @route('/<user_id>', methods=['DELETE'])
    @token_required
    def delete_user(self, user_id):
        UserService().delete_user(user_id)
        return 204
    
    @route('/<user_id>/follow', methods=['POST'])
    @token_required
    def follow_user(self, user_id):
        service_data = UserService().follow_user(user_id)
        return service_data.to_json(), 200
    
    @route('/<user_id>/unfollow', methods=['POST'])
    @token_required
    def unfollow_user(self, user_id):
        UserService().unfollow_user(user_id)
        return 204
    
    @route('/<user_id>/followers', methods=['GET'])
    @token_required
    def get_followers(self, user_id):
        page = request.args.get('page', 1, int)
        service_data = UserService().get_followers(user_id, page)
        return [follower.to_quickview() for follower in service_data], 200
    
    @route('/<user_id>/following', methods=['GET'])
    @token_required
    def get_followings(self, user_id):
        page = request.args.get('page', 1, int)
        service_data = UserService().get_followings(user_id, page)
        return [following.to_quickview() for following in service_data], 200
    
    @route('/<user_id>/friends', methods=['GET'])
    @token_required
    def get_friends(self, user_id):
        page = request.args.get('page', 1, int)
        service_data = FriendshipService().get_friends(user_id, page)
        return [serialize_friend(friend.friendship_id, friend[0]) for friend in service_data], 200
    
def serialize_friend(friendship_id, user):
    user_json = user.to_quickview()
    user_json["friendship_id"] = friendship_id
    user_json["friendship_status"] = "accepted"
    return user_json
