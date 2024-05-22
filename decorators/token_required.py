import jwt
import os
from dotenv import load_dotenv
from flask import g, request
from functools import wraps
from constants.error_constants import  UnauthorizedError

load_dotenv()


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
            g.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError
        except jwt.InvalidTokenError:
            raise UnauthorizedError

        return f(*args, **kwargs)

    return decorated_function
