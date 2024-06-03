import pytest
from tests.unittests.api.api_unit_test import APIUnitTest
from unittest.mock import patch
from tests.mocks.user_service import MockUserService

class TestSearchAPIs(APIUnitTest):    
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.search.UserService', new=MockUserService):
            yield
    
    def test_login(self, client):
        response = client.get('/search?query=johndoe')
        assert response.status_code == 200
        assert response.json == [{
            "username": "johndoe",
            "email": "john.doe@example.com",
            "name": "John Doe",
            "profile_pic": "https://example.com/johndoe.jpg"
        }, {
            "username": "janedoe",
            "email": "jane.doe@example.com",
            "name": "Jane Doe",
            "profile_pic": "https://example.com/janedoe.jpg"
        }]
