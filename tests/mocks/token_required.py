from flask import g
from functools import wraps


# Mock implementation for testing
def mock_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Simulate token validation
        g.user_id = 'mock_user_id'
        return f(*args, **kwargs)

    return decorated_function