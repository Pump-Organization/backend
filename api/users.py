from flask_classful import FlaskView, route
from flask import request
from decorators.token_required import token_required
from services.user_service import UserService

class UsersView(FlaskView):
    route_base = 'users'
    
    @route('', methods=['POST'])
    def create_user(self):
        request_data = request.get_json()
        service_response = UserService().create_user(request_data)
        return service_response.data.to_json(), service_response.status_code
    
    @route('/<user_id>', methods=['GET'])
    def get_user(self, user_id):
        service_response = UserService().get_user(user_id)
        return service_response.data.to_json(), service_response.status_code

    @route('/<user_id>', methods=['PATCH'])
    @token_required
    def update_user(self, user_id):
        request_data = request.get_json()
        service_response = UserService().update_user(user_id, data=request_data)
        return service_response.data.to_json(), service_response.status_code

    @route('/<user_id>', methods=['DELETE'])
    def delete_user(self, user_id):
        service_response = UserService().delete_user(user_id)
        return service_response.data, service_response.status_code
    