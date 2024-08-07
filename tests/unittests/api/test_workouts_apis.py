import json
import pytest
from tests.mocks.workout_service import MockWorkoutService
from tests.mocks.attendee_service import MockAttendeeService
from tests.unittests.api.api_unit_test import APIUnitTest
from unittest.mock import patch


class TestWorkoutAPIs(APIUnitTest):    
    @pytest.fixture(autouse=True)
    def mocks(self):
        with patch('api.workouts.WorkoutService', new=MockWorkoutService), \
             patch('api.workouts.AttendeeService', new=MockAttendeeService):
            yield

    def test_create_workout(self, client):
        data = {
            "title": "Morning Run",
            "description": "Morning run around the park"
        }
        response = client.post('/workouts', json=data)
        assert response.status_code == 200
        assert response.json == {
            "title": "Morning Run",
            "description": "Morning run around the park"
        }

    def test_get_workout(self, client):
        response = client.get('/workouts/1')
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "title": "Morning Run",
            "description": "Morning run around the park"
        }

    def test_update_workout(self, client):
        data = {
            "title": "Morning Jog"
        }
        response = client.patch('/workouts/1', json=data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "title": "Morning Jog",
            "description": "Morning run around the park"
        }

    def test_delete_workout(self, client):
        response = client.delete('/workouts/1')
        assert response.status_code == 204

    def test_get_upcoming_workouts(self, client):
        response = client.get('/workouts/upcoming?date=08/01/21')
        assert response.status_code == 200
        assert json.loads(response.data) == [{
            "title": "Morning Run",
            "description": "Morning run around the park"
        }]
    
    def test_get_invites(self, client):
        response = client.get('/workouts/invites?date=08/01/21')
        assert response.status_code == 200
        assert json.loads(response.data) == [{
            "title": "Morning Run",
            "description": "Morning run around the park"
        }]

    def test_list_workout_attendees(self, client):
        response = client.get('/workouts/1/users')
        assert response.status_code == 200
        assert json.loads(response.data) == [{
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "johndoe",
            "profile_pic": "https://example.com/johndoe.jpg"
        }]

    def test_accept_workout(self, client):
        response = client.post('/workouts/1/accept', json={})
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "attendee_id": 1,
            "workout_id": 1,
            "user_id": 1,
            "attendee_type": "guest",
            "status": "accepted"
        }

    def test_reject_workout(self, client):
        response = client.post('/workouts/1/reject', json={})
        assert response.status_code == 204
