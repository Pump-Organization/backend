from constants.error_constants import NotFoundError, ForbiddenError
from db.db import db
from flask import g
from functools import wraps
from db.models.follower import Follower, FollowStatusEnum
from db.models.user import User, PrivacySettingEnum


def check_privacy(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs.get("user_id")
        if user_id == g.user_id:
            return f(*args, **kwargs)
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError
        if user.privacy_setting == PrivacySettingEnum.public:
            return f(*args, **kwargs)

        follow = (
            db.session.query(Follower)
            .filter(
                Follower.follower_id == g.user_id,
                Follower.followed_id == user_id,
                Follower.status == FollowStatusEnum.accepted,
            )
            .first()
        )
        if follow:
            return f(*args, **kwargs)
        raise ForbiddenError

    return decorated_function
