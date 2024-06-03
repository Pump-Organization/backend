from services.auth_service import AuthService

class MockAuthService(AuthService):
    def __init__(self) -> None:
        super().__init__()

    def login(self, data):
        return self.ServiceResponse(status_code=200, data={"token": "mock_token"})