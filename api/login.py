from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import reset_password_token_required
from services.auth_service import AuthService
from services.user_service import UserService


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

    @route('forgot_password', methods=['POST'])
    def forgot_password(self):
        request_data = request.get_json()
        email = request_data.get('email')
        AuthService().send_forgot_password_email(email)
        return "", 204

    @route('reset-password', methods=['POST'])
    @reset_password_token_required
    def reset_password(self):
        request_data = request.get_json()
        UserService().reset_password(request_data.get('password'))
        return "", 204
