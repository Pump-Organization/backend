import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from constants.error_constants import UnauthorizedError
from db.models.user import User
from services.service import Service


load_dotenv()


class AuthService(Service):
    def __init__(self) -> None:
        super().__init__(User)
    
    def login(self, data):
        username = data.get('username')
        user = self.query_by_attribute(username=username)
        if not user or not self.check_password(user.data, data.get('password')):
            raise UnauthorizedError("login error, invalid credentials")
        
        token = self.generate_jwt_token(user.data.id)
        return self.ServiceResponse(status_code=200, data={'token': token})


    def check_password(self, user, password):
        hashed_password = user.hashed_password
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
        
    def generate_jwt_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        return jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
