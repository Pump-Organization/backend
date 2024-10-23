class TestBasicTests:
    def test_basic(self):
        assert 1 == 1

    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.text == 'testing'
