import json
import pytest
from tests.unittests.api_unit_test import APIUnitTest
from unittest.mock import patch
from tests.mocks.profile_service import MockProfileService



class TestFeedAPIs(APIUnitTest):
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.feed.ProfileService', new=MockProfileService):
            yield

    def test_get_feed(self, client):
        response = client.get('/feed')
        assert response.status_code == 200
        assert json.loads(response.data) == [{
            "title": "Morning Run",
            "description": "Morning run around the park",
            "workout_type": "run"
        }]
