from argon2 import PasswordHasher
from flask import g
from constants.error_constants import BadDataError, ConflictError, ForbiddenError, NotFoundError
from constants import USERS_PER_PAGE
from db.models.user import User
from db.models.follower import Follower
from db.models.friendship import Friendship
from services.service import Service
from sqlalchemy import String, case, and_, or_, func
from sqlalchemy.orm import aliased
from logging import getLogger

logger = getLogger(__name__)


class UserService(Service):
    def __init__(self) -> None:
        super().__init__(User)

    def create_user(self, data):
        if User.query.filter_by(username=data.get('username')).first():
            raise ConflictError("username taken")
        if User.query.filter_by(email=data.get('email')).first():
            raise ConflictError("email taken")

        password = self.set_password(data.get('password'))
        new_user = User(
            username = data.get('username'),
            name = data.get('name'),
            profile_pic = data.get('profile_pic'),
            location = data.get('location'),
            email = data.get('email'),
            bio = data.get('bio'),
            hashed_password = password
        )
        return self.add_data(new_user)
    
    def get_user(self, user_id):
        return self.get_data(user_id)
    
    def update_user(self, user_id, data):
        try:
            if g.user_id != int(user_id):
                raise ForbiddenError
            user = self.session.query(User).filter(User.id==user_id).first()
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                self.session.commit()
                return self.ServiceResponse(status_code=200, data=user)
            else:
                raise NotFoundError
        except Exception as e:
            return self.handle_error(e)
    
    def delete_user(self, user_id):
        try:
            if g.user_id != int(user_id):
                raise ForbiddenError
            self.session.query(User).filter(User.id==user_id).delete()
            self.session.commit()
            return self.ServiceResponse(status_code=204)
        except Exception as e:
            return self.handle_error(e)
    
    def set_password(self, password):
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        return hashed_password
    
    def follow_user(self, user_id):
        try:
            if g.user_id == int(user_id):
                raise BadDataError("cannot follow self")
            if Follower.query.filter_by(follower_id=g.user_id, followed_id=user_id).first():
                raise ConflictError("already following")
            new_follower = Follower(
                follower_id = g.user_id,
                followed_id = user_id
            )
            return self.add_data(new_follower)
        except Exception as e:
            return self.handle_error(e)
    
    def search_users(self, query, page=1):
        # Define the case statement for conditional status modification
        status_case = case(
            (and_(Friendship.status == 'requested', Friendship.recipient_id == g.user_id), 'pending'),
            (and_(Friendship.status == 'requested', Friendship.sender_id == g.user_id), 'requested'),
            (or_(Friendship.status == 'accepted'), 'accepted'),
            else_=func.cast('none', String)
        )

        # Perform the user search query
        users_query = self.session.query(User, Friendship.id.label('friendship_id'), status_case.label('friendship_status'))\
            .outerjoin(Friendship, or_(
                and_(Friendship.sender_id == User.id, Friendship.recipient_id == g.user_id),
                and_(Friendship.recipient_id == User.id, Friendship.sender_id == g.user_id)
            ))\
            .filter(User.username.ilike(f'%{query}%')).distinct(User.id)

        # Execute the query and paginate results
        results = users_query.paginate(page=page, per_page=20).items
        logger.info(f"####### Search results: {results}")

        return self.ServiceResponse(status_code=200, data=results)
        