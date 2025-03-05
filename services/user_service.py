import logging
import traceback
import uuid
from argon2 import PasswordHasher
from flask import g
from constants.error_constants import (
    BadDataError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)
from settings import USERS_PER_PAGE
from db.models.user import User
from db.models.follower import Follower, FollowStatusEnum
from services.event_emitter_service import EventEmitterService
from services.service import Service
from sqlalchemy import case, and_
from utils.user_utils import is_user_public


class UserService(Service):
    def __init__(self) -> None:
        super().__init__(User)

    def create_user(self, data):
        if User.query.filter_by(username=data.get("username")).first():
            raise ConflictError("username taken")
        if User.query.filter_by(email=data.get("email")).first():
            raise ConflictError("email taken")

        password = self.set_password(data.get("password"))
        new_user = User(
            username=data.get("username"),
            name=data.get("name"),
            profile_pic=data.get("profile_pic"),
            location=data.get("location"),
            email=data.get("email"),
            bio=data.get("bio"),
            hashed_password=password,
        )
        return self.add_data(new_user)

    def get_user(self, user_id) -> User:
        return self.get_data(user_id)

    def update_user(self, user_id, data):
        if g.user_id != uuid.UUID(user_id):
            raise ForbiddenError
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            self.session.commit()
            return user
        else:
            raise NotFoundError

    def reset_password(self, new_password):
        user = self.get_data(g.user_id)
        user.hashed_password = self.set_password(new_password)
        self.session.commit()
        return

    def delete_user(self, user_id):
        if g.user_id != uuid.UUID(user_id):
            raise ForbiddenError
        self.session.query(User).filter(User.id == user_id).delete()
        self.session.commit()
        return

    def set_password(self, password):
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        return hashed_password

    def follow_user(self, user_id):
        if g.user_id == uuid.UUID(user_id):
            raise BadDataError("cannot follow self")
        if Follower.query.filter_by(follower_id=g.user_id, followed_id=user_id).first():
            raise ConflictError("already following")

        is_public = is_user_public(user_id)

        if is_public:
            new_follower = Follower(
                follower_id=g.user_id,
                followed_id=user_id,
                status=FollowStatusEnum.accepted,
            )
        else:
            new_follower = Follower(
                follower_id=g.user_id,
                followed_id=user_id,
                status=FollowStatusEnum.pending,
            )

        # add follower to db
        response = self.add_data(new_follower)

        if is_public:
            event_name = "FOLLOW-CREATED"
        else:
            event_name = "FOLLOW_REQUEST-CREATED"

        try:
            follower = self.get_user(g.user_id)
            # emit event on successful transaction
            EventEmitterService().emit_event(
                {
                    "name": event_name,
                    "data": {
                        "created_at": str(response.created_at),
                        "subject_id": follower.id.hex,
                        "subject_username": follower.username,
                        "target_id": user_id,
                    },
                }
            )
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return response

    def unfollow_user(self, user_id):
        if g.user_id == uuid.UUID(user_id):
            raise BadDataError("cannot unfollow self")
        follower = Follower.query.filter_by(
            follower_id=g.user_id, followed_id=user_id
        ).first()
        if follower:
            self.session.delete(follower)
            self.session.commit()

            try:
                follower = self.get_user(g.user_id)
                EventEmitterService().emit_event(
                    {
                        "name": "FOLLOW-DELETED",
                        "data": {
                            "target_id": user_id,
                            "created_at": str(follower.created_at),
                        },
                    }
                )
            except Exception:
                logging.critical("### Error emitting event")
                logging.critical(traceback.format_exc())

        return

    def get_followers(self, user_id, page=1):
        followers = (
            self.session.query(User)
            .join(Follower, Follower.follower_id == User.id)
            .filter(
                Follower.followed_id == user_id,
                Follower.status == FollowStatusEnum.accepted,
            )
            .paginate(page=page, per_page=USERS_PER_PAGE)
            .items
        )
        return followers

    def get_follow_requests(self, page=1):
        follow_requests = (
            self.session.query(User)
            .join(Follower, Follower.follower_id == User.id)
            .filter(
                Follower.followed_id == g.user_id,
                Follower.status == FollowStatusEnum.pending,
            )
            .paginate(page=page, per_page=USERS_PER_PAGE)
            .items
        )
        return follow_requests

    def get_followings(self, user_id, page=1):
        followings = (
            self.session.query(User)
            .join(Follower, Follower.followed_id == User.id)
            .filter(
                Follower.follower_id == user_id,
                Follower.status == FollowStatusEnum.accepted,
            )
            .paginate(page=page, per_page=USERS_PER_PAGE)
            .items
        )
        return followings

    def search_users(self, query, page=1):
        is_following = case(
            (
                and_(
                    Follower.followed_id == User.id, Follower.follower_id == g.user_id
                ),
                True,
            ),
            else_=False,
        )

        follow_status = case(
            (
                and_(
                    Follower.followed_id == User.id,
                    Follower.follower_id == g.user_id,
                    Follower.status == FollowStatusEnum.accepted,
                ),
                "yes",
            ),
            (
                and_(
                    Follower.followed_id == User.id,
                    Follower.follower_id == g.user_id,
                    Follower.status == FollowStatusEnum.pending,
                ),
                "pending",
            ),
            else_="no",
        )

        users_query = (
            self.session.query(User, is_following, follow_status)
            .outerjoin(Follower, User.id == Follower.followed_id)
            .filter(User.username.ilike(f"%{query}%"))
        )
        results = users_query.paginate(page=page, per_page=USERS_PER_PAGE).items
        return results

    def is_following_user(self, follower_id):
        return (
            Follower.query.filter_by(
                follower_id=g.user_id, followed_id=follower_id
            ).first()
            is not None
        )

    def get_num_followers(self, user_id):
        num_followers = Follower.query.filter_by(followed_id=user_id).count()
        return num_followers

    def get_num_followings(self, user_id):
        num_followings = Follower.query.filter_by(follower_id=user_id).count()
        return num_followings
