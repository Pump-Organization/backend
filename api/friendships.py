from flask_classful import FlaskView, route
from flask import jsonify, request
from services.friendship_service import FriendshipService

class FriendshipsView(FlaskView):
    route_base = 'friendships'

    @route('', methods=['POST'])
    def create_friendship(self):
        request_data = request.get_json()
        service_response = FriendshipService().create_friendship(request_data)
        return jsonify(service_response.data), service_response.status_code
    
    @route('/<friendship_id>', methods=['GET'])
    def get_friendship(self, friendship_id):
        service_response = FriendshipService().get_friendship(friendship_id)
        return jsonify(service_response.data), service_response.status_code

    @route('/<friendship_id>', methods=['PATCH'])
    def update_friendship(self, friendship_id):
        request_data = request.get_json()
        service_response = FriendshipService().update_friendship(friendship_id, data=request_data)
        return jsonify(service_response.data), service_response.status_code

    @route('/<friendship_id>', methods=['DELETE'])
    def delete_friendship(self, friendship_id):
        service_response = FriendshipService().delete_friendship(friendship_id)
        return jsonify(service_response.data), service_response.status_code
