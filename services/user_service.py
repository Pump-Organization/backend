from db.models.user import User
from services.service import Service


class UserService(Service):
    def __init__(self) -> None:
        super().__init__(User)

    def create_user(self, data):
        new_user = User(
            username = data.get('username'),
            name = data.get('name'),
            profile_pic = data.get('profile_pic'),
            location = data.get('location'),
            email = data.get('email'),
            bio = data.get('bio')
        )
        return self.add_data(new_user)
    
    def get_user(self, user_id):
        return self.get_data(user_id)
    
    def update_user(self, user_id, data):
        return self.update_data(id=user_id, updated_data=data)
    
    def delete_user(self, user_id):
        return self.delete_data(user_id)
        