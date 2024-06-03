import json
import pytest
from tests.mocks.profile_service import MockProfileService
from tests.unittests.api_unit_test import APIUnitTest
from unittest.mock import patch


class TestProfileAPIs(APIUnitTest):    
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.profiles.ProfileService', new=MockProfileService):
            yield
    
    def test_get_profile(self, client):
        response = client.get('/profiles/1')
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe",
            "profile_pic": "https://example.com/johndoe.jpg",
            "num_friends": 2,
            "workout_counts": {"run": 2, "lift": 1, "bike": 1}
        }

    def test_get_profile_workouts(self, client):
        response = client.get('/profiles/1/workouts')
        assert response.status_code == 200
        assert json.loads(response.data) == [{
            "title": "Morning Run",
            "description": "Morning run around the park",
            "workout_type": "run"
        }]

    