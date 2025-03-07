import jwt
import settings
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from constants.email_constants import (
    FORGOT_PASSWORD_BODY_HTML,
    FORGOT_PASSWORD_BODY_TEXT,
    FORGOT_PASSWORD_SUBJECT,
)  # noqa E501
from datetime import datetime, timedelta, timezone
from constants.error_constants import BadDataError, UnauthorizedError
from db.models.user import User
from db.models.refresh_token import RefreshToken
from services.service import Service
from services.email_service import EmailService
from services.user_service import UserService


class AuthService(Service):
    def __init__(self) -> None:
        super().__init__(User)

    def login(self, data):
        username = data.get("username")
        user = self.query_by_attribute(username=username)
        if not user or not self.check_password(user, data.get("password")):
            raise UnauthorizedError
        token = self.generate_jwt_token(user.id.hex)
        refresh_token, expires_at = self.generate_refresh_token(user.id.hex)
        self.store_refresh_token(refresh_token, user.id.hex, expires_at)
        return {
            "token": token,
            "refresh_token": refresh_token,
        }

    def check_password(self, user, password):
        ph = PasswordHasher()
        try:
            ph.verify(user.hashed_password, password)
        except VerificationError:
            return False

        if ph.check_needs_rehash(user.hashed_password):
            user.hashed_password = UserService().set_password(password)
            self.session.commit()
        return True

    def generate_jwt_token(
        self, user_id, expires_at=10, encode_key=settings.JWT_SECRET, extra_payload={}
    ):  # noqa E501
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_at),
        }
        for key, value in extra_payload.items():
            payload[key] = value
        return jwt.encode(payload, encode_key, algorithm="HS256")

    def generate_refresh_token(self, user_id):
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        payload = {"user_id": user_id, "exp": expires_at}
        refresh_token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        return refresh_token, expires_at

    def store_refresh_token(self, refresh_token, user_id, expires_at):
        old_refresh_token = (
            self.session.query(RefreshToken).filter_by(user_id=user_id).one_or_none()
        )
        if old_refresh_token:
            self.session.delete(old_refresh_token)
        refresh_token = RefreshToken(
            token=refresh_token, user_id=user_id, expires_at=expires_at
        )
        self.session.add(refresh_token)
        self.session.commit()

    def refresh_access_token(self, refresh_token):
        # decode the refresh token and check if it is valid
        if self.session.query(RefreshToken).filter_by(token=refresh_token).count() == 0:
            return None

        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_SECRET, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return None  # refresh token has expired, don't log as error
        user_id = payload["user_id"]
        user = self.session.query(User).filter(User.id == user_id)
        if not user:
            return None
        return {"token": self.generate_jwt_token(user_id)}

    def generate_forgot_password_token(self, email):
        user = self.query_by_attribute(email=email)
        if not user:
            raise BadDataError("Email not found")
        token = self.generate_jwt_token(
            user.id.hex,
            expires_at=15,
            encode_key=settings.FORGOT_PASSWORD_SECRET,
            extra_payload={"email": email},
        )
        return {"token": token}

    def send_forgot_password_email(self, email):
        token = self.generate_forgot_password_token(email).get("token")
        url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        body_text = FORGOT_PASSWORD_BODY_TEXT(url)
        body_html = FORGOT_PASSWORD_BODY_HTML(url)
        EmailService().send_email(email, FORGOT_PASSWORD_SUBJECT, body_text, body_html)
        return
