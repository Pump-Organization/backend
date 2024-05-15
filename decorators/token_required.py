import jwt
import os
from dotenv import load_dotenv
from flask import request, jsonify
from functools import wraps
from constants.error_constants import ErrorConstants

load_dotenv()


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Expecting 'Bearer <token>'
            token = token.split()[1]
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return ErrorConstants.UNAUTHORIZED, 401
        except jwt.InvalidTokenError:
            return ErrorConstants.UNAUTHORIZED, 401

        return f(*args, **kwargs)

    return decorated_function
