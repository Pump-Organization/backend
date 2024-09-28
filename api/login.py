from flask_classful import FlaskView, route
from flask import request
from services.auth_service import AuthService

class LoginView(FlaskView):
    route_base = 'login'

    @route('', methods=['POST'])
    def login(self):
        request_data = request.get_json()
        service_data = AuthService().login(request_data)
        return service_data, 200
    
    @route('refresh', methods=['POST'])
    def refresh(self):
        refresh_token = request.get_json().get('refresh_token')
        service_data = AuthService().refresh_access_token(refresh_token)
        return service_data, 200
