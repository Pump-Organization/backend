from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import reset_password_token_required
from services.auth_service import AuthService
from services.user_service import UserService
from schemas.auth import (
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    RefreshTokenRequest,
)


class LoginView(FlaskView):
    route_base = "login"

    @route("", methods=["POST"])
    def login(self):
        request_data = request.get_json()
        validated_data = LoginRequest(**request_data)
        service_data = AuthService().login(validated_data.model_dump())
        return service_data, 200

    @route("/refresh", methods=["POST"])
    def refresh(self):
        request_data = request.get_json()
        validated_data = RefreshTokenRequest(**request_data)
        service_data = AuthService().refresh_access_token(validated_data.refresh_token)
        if not service_data:
            return "Unauthorized", 401
        return service_data, 200

    @route("/forgot_password", methods=["POST"])
    def forgot_password(self):
        request_data = request.get_json()
        validated_data = ForgotPasswordRequest(**request_data)
        AuthService().send_forgot_password_email(validated_data.email)
        return "", 204

    @route("/reset-password", methods=["POST"])
    @reset_password_token_required
    def reset_password(self):
        request_data = request.get_json()
        validated_data = ResetPasswordRequest(**request_data)
        UserService().reset_password(validated_data.password)
        return "", 204
