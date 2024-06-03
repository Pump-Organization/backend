from tests.mocks.token_required import mock_token_required
from unittest.mock import patch
patch('middleware.token_required.token_required', new=mock_token_required).start()

import json
import pytest
from tests.mocks.friendship_service import MockFriendshipService
from tests.unittests.api_unit_test import APIUnitTest


class TestFriendshipAPIs(APIUnitTest):
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.friendships.FriendshipService', new=MockFriendshipService):
            yield

    def test_create_friendship(self, client):
        response = client.post('/friendships', json={"recipient_id": 1})
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "friendship_id": 1,
            "sender_id": 1,
            "recipient_id": 2,
            "status": "pending"
        }

    def test_get_friendship(self, client):
        response = client.get('/friendships/1')
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "friendship_id": 1,
            "sender_id": 1,
            "recipient_id": 2,
            "status": "pending"
        }

    def test_update_friendship(self, client):
        response = client.patch('/friendships/1', json={"status": "accepted"})
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "friendship_id": 1,
            "sender_id": 1,
            "recipient_id": 2,
            "status": "accepted"
        }

    def test_delete_friendship(self, client):
        response = client.delete('/friendships/1')
        assert response.status_code == 204

    def test_get_friend_requests(self, client):
        response = client.get('/friendships/requests')
        assert response.status_code == 200
        assert json.loads(response.data) == [{
            "friendship_id": 2,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "username": "janedoe",
            "profile_pic": "https://example.com/janedoe.jpg"
        }]
