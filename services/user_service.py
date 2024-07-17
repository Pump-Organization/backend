from argon2 import PasswordHasher
from flask import g
from constants.error_constants import ForbiddenError, NotFoundError, ConflictError
from constants import USERS_PER_PAGE
from db.models.user import User
from db.models.friendship import Friendship
from services.service import Service
from sqlalchemy import String, case, and_, or_, func
from sqlalchemy.orm import aliased


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
    
    def search_users(self, query, page=1):
        # Define aliases for sender and recipient to use in the subquery
        sender_alias = aliased(Friendship)
        recipient_alias = aliased(Friendship)

        # Define the case statement for conditional status modification
        status_case = case(
            (and_(recipient_alias.status == 'requested', recipient_alias.recipient_id == g.user_id), 'pending'),
            (or_(sender_alias.status == 'accepted', recipient_alias.status == 'accepted'), 'accepted'),
            (and_(sender_alias.status == 'requested', sender_alias.sender_id == g.user_id), 'requested'),
            else_=func.cast('unknown', String)
        )

        # Define the friendship subquery
        friendship_subquery = self.session.query(
            sender_alias.recipient_id.label('user_id'),
            sender_alias.id.label('friendship_id'),
            status_case.label('status')
        ).filter(sender_alias.sender_id == g.user_id).union(
            self.session.query(
                recipient_alias.sender_id.label('user_id'),
                recipient_alias.id.label('friendship_id'),
                status_case
            ).filter(recipient_alias.recipient_id == g.user_id)
        ).subquery('friendship_status')

        # Perform the user search query
        users_query = self.session.query(User).filter(User.username.ilike(f'%{query}%'))

        # Join the user search results with the friendship subquery
        final_query = users_query.outerjoin(
            friendship_subquery,
            User.id == friendship_subquery.c.user_id
        ).add_columns(
            friendship_subquery.c.status,
            friendship_subquery.c.friendship_id
        )

        # Execute the query and paginate results
        results = final_query.paginate(page=page, per_page=20).items

        return self.ServiceResponse(status_code=200, data=results)
        