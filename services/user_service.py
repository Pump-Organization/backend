import bcrypt
from db.models.user import User
from services.service import Service


class UserService(Service):
    def __init__(self) -> None:
        super().__init__(User)

    def create_user(self, data):
        salt, password = self.set_password(data.get('password'))
        new_user = User(
            username = data.get('username'),
            name = data.get('name'),
            profile_pic = data.get('profile_pic'),
            location = data.get('location'),
            email = data.get('email'),
            bio = data.get('bio'),
            salt = salt,
            hashed_password = password
        )
        return self.add_data(new_user)
    
    def get_user(self, user_id):
        return self.get_data(user_id)
    
    def update_user(self, user_id, data):
        return self.update_data(id=user_id, updated_data=data)
    
    def delete_user(self, user_id):
        return self.delete_data(user_id)
    
    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        decoded_salt = salt.decode('utf-8')

        return decoded_salt, hashed_password
        