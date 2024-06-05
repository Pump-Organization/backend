from flask_classful import FlaskView, route
from flask import g, request
from middleware.token_required import token_required
from services.friendship_service import FriendshipService

class FriendshipsView(FlaskView):
    route_base = 'friendships'

    @route('', methods=['POST'])
    @token_required
    def create_friendship(self):
        request_data = request.get_json()
        request_data['sender_id'] = g.user_id
        service_response = FriendshipService().create_friendship(request_data)
        return service_response.data.to_json(), service_response.status_code
    
    @route('/<friendship_id>', methods=['GET'])
    def get_friendship(self, friendship_id):
        service_response = FriendshipService().get_friendship(friendship_id)
        return service_response.data.to_json(), service_response.status_code

    @route('/<friendship_id>', methods=['PATCH'])
    @token_required
    def update_friendship(self, friendship_id):
        request_data = request.get_json()
        service_response = FriendshipService().update_friendship(friendship_id, data=request_data)
        return service_response.data.to_json(), service_response.status_code

    @route('/<friendship_id>', methods=['DELETE'])
    @token_required
    def delete_friendship(self, friendship_id):
        service_response = FriendshipService().delete_friendship(friendship_id)
        return service_response.data, service_response.status_code
    
    @route('/requests', methods=['GET'])
    @token_required
    def get_friend_requests(self): # TODO: Add pagination
        page = request.args.get('page', 1, int)
        service_response = FriendshipService().get_friend_requests(page)
        return [serialize_friend(friend_request.friendship_id, friend_request[0]) for friend_request in service_response.data]
    

def serialize_friend(friendship_id, user):
    user_json = user.to_quickview()
    user_json["friendship_id"] = friendship_id
    return user_json
