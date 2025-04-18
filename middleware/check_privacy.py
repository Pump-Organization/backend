import uuid
from constants.error_constants import NotFoundError, ForbiddenError
from db.db import db
from flask import g
from functools import wraps
from db.models.attendee import Attendee
from db.models.follower import Follower, FollowStatusEnum
from db.models.user import User, PrivacySettingEnum
from services.workout_service import WorkoutService, Workout


def check_privacy(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs.get("user_id")
        if g.get("blocked_users") and user_id in g.blocked_users:
            raise NotFoundError
        if uuid.UUID(user_id) == g.user_id:
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


def check_workout_privacy(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        workout_id = kwargs.get("workout_id")
        workout = db.session.get(Workout, workout_id)
        if not workout:
            raise NotFoundError

        user_id = WorkoutService().get_organizer_id(workout_id)

        # Allow if the requester is the organizer
        if user_id == g.user_id:
            return f(*args, **kwargs)

        user = db.session.get(user_id)
        if not user:
            raise NotFoundError

        # Allow if the organizer is public
        if user.privacy_setting == PrivacySettingEnum.public:
            return f(*args, **kwargs)

        # Allow if the requester follows the organizer
        follow = Follower.query.filter_by(
            follower_id=g.user_id, followed_id=user_id, status=FollowStatusEnum.accepted
        ).first()
        if follow:
            return f(*args, **kwargs)

        # Allow if the requester follows any attendee or any attendee is public
        attendee_ids = (
            db.session.query(Attendee.user_id).filter_by(workout_id=workout_id).all()
        )
        attendee_ids = {attendee_id for (attendee_id,) in attendee_ids}
        for attendee_id in attendee_ids:
            attendee_user = User.query.get(attendee_id)
            if attendee_user and attendee_user.privacy_setting == PrivacySettingEnum.public:  # fmt: skip
                # Allow access if any attendee is public
                return f(*args, **kwargs)

        following_attendee = Follower.query.filter(
            Follower.follower_id == g.user_id,
            Follower.followed_id.in_(attendee_ids),
            Follower.status == FollowStatusEnum.accepted,
        ).first()

        if following_attendee:
            return f(*args, **kwargs)

        raise ForbiddenError

    return decorated_function
