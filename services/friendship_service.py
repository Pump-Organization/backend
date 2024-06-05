from services.service import Service
from db.models.friendship import Friendship, FriendshipStatusEnum
from db.models.user import User
from constants.error_constants import ForbiddenError, NotFoundError
from sqlalchemy import and_
from flask import g


class FriendshipService(Service):
    def __init__(self) -> None:
        super().__init__(Friendship)

    def create_friendship(self, data):
        friendship = Friendship(
            sender_id = g.user_id,
            recipient_id = data.get('recipient_id'),
            status = FriendshipStatusEnum.requested
        )
        return self.add_data(friendship)
    
    def get_friendship(self, friendship_id):
        return self.get_data(friendship_id)
    
    def update_friendship(self, friendship_id, data):
        try:
            friendship = self.model.query.get(friendship_id)
            if not friendship:
                raise NotFoundError
            if g.user_id != friendship.recipient_id:
                raise ForbiddenError
            for key, value in data.items():
                setattr(friendship, key, value)
            self.session.commit()
            return self.ServiceResponse(status_code=200, data=friendship)
        except Exception as e:
            return self.handle_error(e)
    
    def delete_friendship(self, friendship_id):
        try:
            friendship = self.model.query.get(friendship_id)
            if not friendship:
                return self.ServiceResponse(status_code=204)
            if g.user_id not in (friendship.sender_id, friendship.recipient_id):
                raise ForbiddenError
            self.session.delete(friendship)
            self.session.commit()
            return self.ServiceResponse(status_code=204)
        except Exception as e:
            return self.handle_error(e)
    
    def get_frienship_count(self, user_id):
        num_friendships = Friendship.query.filter(
            (Friendship.sender_id == user_id) | (Friendship.recipient_id == user_id),
            Friendship.status ==  FriendshipStatusEnum.accepted
        ).count()
        return self.ServiceResponse(status_code=200, data=num_friendships)
    
    def get_friends(self, user_id):
        friends = self.session.query(User, Friendship.id.label("friendship_id")).join(Friendship, Friendship.sender_id == User.id).filter(
            and_(
                Friendship.recipient_id == user_id,
                Friendship.status == FriendshipStatusEnum.accepted
            )
        ).union(
            self.session.query(User, Friendship.id.label("friendship_id")).join(Friendship, Friendship.recipient_id == User.id).filter(
                and_(
                    Friendship.sender_id == user_id,
                    Friendship.status == FriendshipStatusEnum.accepted
                )
            )
        ).all()
        return self.ServiceResponse(status_code=200, data=friends)
    
    def get_friend_requests(self):
        friend_requests = self.session.query(User, Friendship.id.label("friendship_id")).join(Friendship, Friendship.sender_id == User.id).filter(
            and_(
                Friendship.recipient_id == g.user_id,
                Friendship.status == FriendshipStatusEnum.requested
            )
        ).all()
        return self.ServiceResponse(status_code=200, data=friend_requests)
