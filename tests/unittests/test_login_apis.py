import pytest
from tests.unittests.api_unit_test import APIUnitTest
from unittest.mock import patch
from tests.mocks.auth_service import MockAuthService

class TestLoginAPIs(APIUnitTest):    
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.login.AuthService', new=MockAuthService):
            yield
    
    def test_login(self, client):
        data = {
            "username": "johndoe",
            "password": "password"
        }
        response = client.post('/login', json=data)
        assert response.status_code == 200
        assert response.json == {
            "token": "mock_token"
        }
