from flask_classful import FlaskView, route
from flask import request
from services.auth_service import AuthService

class LoginView(FlaskView):
    route_base = 'login'

    @route('', methods=['POST'])
    def login(self):
        request_data = request.get_json()
        service_response = AuthService().login(request_data)
        return service_response.data, service_response.status_code
