from services.service import Service
from db.models.friendship import Friendship


class FriendshipService(Service):
    def __init__(self) -> None:
        super().__init__(Friendship)

    def create_friendship(self, data):
        friendship = Friendship(
            sender_id = data.get('sender_id'),
            recipient_id = data.get('recipient_id'),
            status = "requested"
        )
        return self.add_data(friendship)
    
    def get_friendship(self, friendship_id):
        return self.get_data(friendship_id)
    
    def update_friendship(self, friendship_id, data):
        return self.update_data(id=friendship_id, updated_data=data)
    
    def delete_friendship(self, friendship_id):
        return self.delete_data(friendship_id)
    
    def get_frienship_count(self, user_id):
        num_friendships = Friendship.query.filter(
            (Friendship.sender_id == user_id) | (Friendship.recipient_id == user_id),
            Friendship.status ==  "accepted"
        ).count()
        return self.ServiceResponse(status_code=200, data=num_friendships)
