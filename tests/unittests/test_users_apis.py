from unittest.mock import patch
import json
import pytest
from tests.mocks.user_service import MockUserService
from tests.mocks.friendship_service import MockFriendshipService
from tests.unittests.api_unit_test import APIUnitTest


class TestUserAPIs(APIUnitTest):
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.users.UserService', new=MockUserService), \
             patch('api.users.FriendshipService', new=MockFriendshipService):
            yield
        

    def test_create_user(self, client):
        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe",
            "profile_pic": "https://example.com/johndoe.jpg"
        }
        response = client.post('/users', json=data)
        assert response.status_code == 200
        assert response.json == {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe",
            "profile_pic": "https://example.com/johndoe.jpg"
        }

    def test_get_user(self, client):
        response = client.get('/users/1')
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe",
            "profile_pic": "https://example.com/johndoe.jpg"
        }

    def test_update_user(self, client):
        data = {
            "name": "John Dope"
        }
        response = client.patch('/users/1', json=data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "name": "John Dope",
            "email": "john.doe@example.com",
            "username": "johndoe",
            "profile_pic": "https://example.com/johndoe.jpg"
        }

    def test_delete_user(self, client):
        response = client.delete('/users/1')
        assert response.status_code == 204

    def test_get_friends(self, client):
        response = client.get('/users/1/friends')
        assert response.status_code == 200
        assert json.loads(response.data) == [
            {
                "friendship_id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "username": "johndoe",
                "profile_pic": "https://example.com/johndoe.jpg"
            },
            {
                "friendship_id": 2,
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "username": "janedoe",
                "profile_pic": "https://example.com/janedoe.jpg"
            }
        ]
