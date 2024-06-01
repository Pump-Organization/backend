from argon2 import PasswordHasher
from flask import g
from constants.error_constants import ForbiddenError, NotFoundError, ConflictError
from db.models.user import User
from services.service import Service


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
            user = self.model.query.get(user_id)
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
        