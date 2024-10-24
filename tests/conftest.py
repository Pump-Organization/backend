import pytest
import uuid
from app import app as flask_app

@pytest.fixture(scope='class')
def app():
    flask_app.config.update({
        'TESTING': True,
    })
    yield flask_app

@pytest.fixture(scope='class')
def client(app):
    return app.test_client()

@pytest.fixture(scope='class')
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='class')
def test_base_user(client):
    test_uuid = uuid.uuid4().hex[:6]
    test_base_user = {
        'email': f'{test_uuid}a@test.com',
        'username': f'{test_uuid}a',
        'password': 'password',
        'name': 'E2E BASE USER'
    }

    test_second_user = {
        'email': f'{test_uuid}b@test.com',
        'username': f'{test_uuid}b',
        'password': 'password',
        'name': 'E2E SECOND USER'
    }

    create_user_response = client.post('/users', json=test_base_user)
    create_second_user_response = client.post('/users', json=test_second_user)
    assert create_user_response.status_code == 200
    test_base_user['id'] = create_user_response.json['id']
    test_second_user['id'] = create_second_user_response.json['id']

    # Authenticate and get JWT token
    auth_response = client.post('/login', json={
        'username': test_base_user['username'],
        'password': test_base_user['password']
    })
    assert auth_response.status_code == 200
    jwt_token = auth_response.json['token']

    second_auth_response = client.post('/login', json={
        'username': test_second_user['username'],
        'password': test_second_user['password']
    })
    assert second_auth_response.status_code == 200
    second_jwt_token = second_auth_response.json['token']

    return {
        'base_user': test_base_user,
        'second_user': test_second_user,
        'token': jwt_token,
        'second_token': second_jwt_token
    }
