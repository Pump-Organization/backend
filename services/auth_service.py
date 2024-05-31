from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from constants.error_constants import UnauthorizedError
from db.models.user import User
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
        if not user or not self.check_password(user.data, data.get('password')):
            raise UnauthorizedError
        
        token = self.generate_jwt_token(user.data.id)
        return self.ServiceResponse(status_code=200, data={'token': token})


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
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
