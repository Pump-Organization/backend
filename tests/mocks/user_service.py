from services.user_service import UserService
from services.service import Service
from tests.mocks.models import MockUser

class MockUserService(UserService):
        def __init__(self) -> None:
            super().__init__()

        def create_user(self, data):
            return Service.ServiceResponse(status_code=200, data=MockUser("John Doe", "john.doe@example.com", "johndoe", "https://example.com/johndoe.jpg"))

        def get_user(self, user_id):
            return Service.ServiceResponse(status_code=200, data=MockUser("John Doe", "john.doe@example.com", "johndoe", "https://example.com/johndoe.jpg"))

        def update_user(self, user_id, data):
            return Service.ServiceResponse(status_code=200, data=MockUser("John Dope", "john.doe@example.com", "johndoe", "https://example.com/johndoe.jpg"))

        def delete_user(self, user_id):
            return Service.ServiceResponse(status_code=204)

        def search_users(self, query, page=1):
            return Service.ServiceResponse(status_code=200, data=[MockUser("John Doe", "john.doe@example.com", "johndoe", "https://example.com/johndoe.jpg"), MockUser("Jane Doe", "jane.doe@example.com", "janedoe", "https://example.com/janedoe.jpg")])
