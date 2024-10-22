import jwt
import os
import uuid
from dotenv import load_dotenv
from flask import g, request
from functools import wraps
from constants.error_constants import UnauthorizedError


flask_env = os.getenv('FLASK_ENV', 'production')
if flask_env == 'development':
    env_path = '.env.development'
else:
    env_path = '.env'
load_dotenv(dotenv_path=env_path)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Token is missing'}, 401

        try:
            # Expecting 'Bearer <token>'
            token = token.split()[1]
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            g.user_id = uuid.UUID(payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError
        except jwt.InvalidTokenError:
            raise UnauthorizedError

        return f(*args, **kwargs)

    return decorated_function


def reset_password_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Token is missing'}, 401
        try:
            # Expecting 'Bearer <token>'
            token = token.split()[1]
            payload = jwt.decode(token, os.getenv('FORGOT_PASSWORD_SECRET'), algorithms=['HS256'])
            g.user_id = uuid.UUID(payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError
        except jwt.InvalidTokenError:
            raise UnauthorizedError
        return f(*args, **kwargs)

    return decorated_function
