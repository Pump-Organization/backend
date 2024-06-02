from services.friendship_service import FriendshipService
from services.service import Service
from tests.mocks.models import MockFriendship
from tests.mocks.models import MockUser
from unittest.mock import MagicMock

class MockFriend:
    def __init__(self, friendship_id, user):
        self.friendship_id = friendship_id
        self.user = user

    def __getitem__(self, item):
        if item == 0:
            return self.user
        raise IndexError('Invalid index')

mock_user1 = MockUser("John Doe", "john.doe@example.com", "johndoe", "https://example.com/johndoe.jpg")
mock_friend1 = MockFriend(1, mock_user1)
mock_user2 = MockUser("Jane Doe", "jane.doe@example.com", "janedoe", "https://example.com/janedoe.jpg")
mock_friend2 = MockFriend(2, mock_user2)

class MockFriendshipService(FriendshipService):
    def __init__(self) -> None:
        super().__init__()

    def get_friends(self, user_id):
        return Service.ServiceResponse(status_code=200, data=[mock_friend1, mock_friend2])
