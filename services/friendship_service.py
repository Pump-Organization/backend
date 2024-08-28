from services.service import Service
from db.models.friendship import Friendship, FriendshipStatusEnum
from db.models.user import User
from constants import USERS_PER_PAGE
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
        friendship = self.model.query.get(friendship_id)
        if not friendship:
            raise NotFoundError
        if g.user_id != friendship.recipient_id:
            raise ForbiddenError
        for key, value in data.items():
            setattr(friendship, key, value)
        self.session.commit()
        return friendship
    
    def delete_friendship(self, friendship_id):
        friendship = self.model.query.get(friendship_id)
        if not friendship:
            return
        if g.user_id not in (friendship.sender_id, friendship.recipient_id):
            raise ForbiddenError
        self.session.delete(friendship)
        self.session.commit()
        return
        
    def is_friend(self, user_id, friend_id):
        friendship = Friendship.query.filter(
            (Friendship.sender_id == user_id) & (Friendship.recipient_id == friend_id) |
            (Friendship.sender_id == friend_id) & (Friendship.recipient_id == user_id)
        ).first()

        if friendship is None:
            return {"status": None, "friendship_id": None}
        elif friendship.status == FriendshipStatusEnum.accepted:
            return {"status": "accepted", "friendship_id": friendship.id}
        else:
            if friendship.sender_id == user_id:
                return {"status": "requested", "friendship_id": friendship.id}
            return {"status": "pending", "friendship_id": friendship.id}
    
    def get_friendship_count(self, user_id):
        num_friendships = Friendship.query.filter(
            (Friendship.sender_id == user_id) | (Friendship.recipient_id == user_id),
            Friendship.status ==  FriendshipStatusEnum.accepted
        ).count()
        return num_friendships
    
    def get_friends(self, user_id, page=1):
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
        ).limit(USERS_PER_PAGE).offset((page - 1) * USERS_PER_PAGE)
        return friends
    
    def get_friend_requests(self, page=1):
        friend_requests = self.session.query(User, Friendship.id.label("friendship_id")).join(Friendship, Friendship.sender_id == User.id).filter(
            and_(
                Friendship.recipient_id == g.user_id,
                Friendship.status == FriendshipStatusEnum.requested
            )
        ).limit(USERS_PER_PAGE).offset((page - 1) * USERS_PER_PAGE)
        return friend_requests
