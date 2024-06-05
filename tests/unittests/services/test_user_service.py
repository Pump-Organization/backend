from app import app as flask_app
import pytest
from unittest.mock import patch, MagicMock
from pytest_mock import mocker
from db.models.user import User
from services.service import Service
from services.user_service import UserService
from constants.error_constants import ConflictError

class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()

    def test_create_user_success(self, user_service, mocker):
        with flask_app.app_context():
            # Mock the User query methods
            mocker.patch('db.models.user.User.query.filter_by', return_value=MagicMock(first=MagicMock(return_value=None)))
            
            # Mock the add_data method
            mocker.patch.object(Service, 'add_data', return_value='mock_user')

            # Mock the set_password method
            mocker.patch.object(UserService, 'set_password', return_value='hashed_password')

            # Test data
            data = {
                'username': 'testcreateuser',
                'email': 'testcreateuser@example.com',
                'password': 'securepassword',
                'name': 'Test User',
                'profile_pic': 'path/to/pic',
                'location': 'Test Location',
                'bio': 'This is a bio'
            }

            result = user_service.create_user(data)
            
            assert result == 'mock_user'
    
    def test_create_user_conflict_username(self, user_service, mocker):
        with flask_app.app_context():
            # Mock the User query methods to return an existing user for username
            mocker.patch('db.models.user.User.query.filter_by', return_value=MagicMock(first=MagicMock(return_value=True)))

            # Test data
            data = {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'securepassword'
            }

            with pytest.raises(ConflictError):
                user_service.create_user(data)

    def test_create_user_conflict_email(self, user_service, mocker):
        with flask_app.app_context():
            # Mock the User query methods to return None for username and an existing user for email
            mocker.patch('db.models.user.User.query.filter_by', side_effect=[
                MagicMock(first=MagicMock(return_value=None)),  # For username check
                MagicMock(first=MagicMock(return_value=True))   # For email check
            ])

            # Test data
            data = {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'securepassword'
            }

            with pytest.raises(ConflictError):
                user_service.create_user(data)

    def test_get_user_success(self, user_service, mocker):
        with flask_app.app_context():
            # Mock the get_data method
            mocker.patch.object(Service, 'get_data', return_value='mock_user')

            user_id = 1
            result = user_service.get_user(user_id)
            
            assert result == 'mock_user'