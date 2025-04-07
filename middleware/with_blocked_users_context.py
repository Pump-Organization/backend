from flask import g
from functools import wraps

from services.user_service import UserService


def with_blocked_users_context(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        blocks = UserService().list_blocks()
        blocks_ids = (
            set((block["blocked_id"].hex) for block in blocks) if blocks else set()
        )

        blocked_by = UserService().list_blocked_by()
        blocked_by_ids = (
            set((block["blocker_id"].hex) for block in blocked_by)
            if blocked_by
            else set()
        )
        g.blocked_users = blocks_ids | blocked_by_ids
        return f(*args, **kwargs)

    return decorated_function
