from tests.mocks.token_required import mock_token_required
from unittest.mock import patch
patch('middleware.token_required.token_required', new=mock_token_required).start()

import pytest
from app import app as flask_app

class APIUnitTest:
    @pytest.fixture
    def client(self):
        return flask_app.test_client()
    