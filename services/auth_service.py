from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from constants.error_constants import UnauthorizedError
from db.models.user import User
from db.models.refresh_token import RefreshToken
from services.service import Service
from services.user_service import UserService


flask_env = os.getenv('FLASK_ENV', 'production')
if flask_env == 'development':
    env_path = '.env.development'
else:
    env_path = '.env'
load_dotenv(dotenv_path=env_path)

class AuthService(Service):
    def __init__(self) -> None:
        super().__init__(User)
    
    def login(self, data):
        username = data.get('username')
        user = self.query_by_attribute(username=username)
        if not user or not self.check_password(user, data.get('password')):
            raise UnauthorizedError
        token = self.generate_jwt_token(user.id.hex)
        refresh_token, expires_at = self.generate_refresh_token(user.id.hex)
        self.store_refresh_token(refresh_token, user.id.hex, expires_at)
        return {
            'token': token,
            'refresh_token': refresh_token,
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
        
    def generate_jwt_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=10)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
    
    def generate_refresh_token(self, user_id):
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        payload = {
            'user_id': user_id,
            'exp': expires_at
        }
        refresh_token = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
        return refresh_token, expires_at
    
    def store_refresh_token(self, refresh_token, user_id, expires_at):
        old_refresh_token = self.session.query(RefreshToken).filter_by(user_id=user_id).one_or_none()
        if old_refresh_token:
            self.session.delete(old_refresh_token)
        refresh_token = RefreshToken(token=refresh_token, user_id=user_id, expires_at=expires_at)
        self.session.add(refresh_token)
        self.session.commit()

    def refresh_access_token(self, refresh_token):
        # decode the refresh token and check if it is valid
        if self.session.query(RefreshToken).filter_by(token=refresh_token).count() == 0:
            raise UnauthorizedError
        
        payload = jwt.decode(refresh_token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
        user_id = payload['user_id']
        user = self.session.query(User).filter(User.id == user_id)
        if not user:
            raise UnauthorizedError
        return {
            'token': self.generate_jwt_token(user_id)
        }
