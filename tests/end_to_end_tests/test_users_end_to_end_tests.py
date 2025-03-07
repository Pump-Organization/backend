import uuid


class TestUsersEndToEndTests:
    test_uuid = uuid.uuid4().hex[:6] + "a"  # only six chars bc field char limits

    expected_user = {
        "email": f"{test_uuid}@test.com",
        "username": test_uuid,
        "name": "E2E Test",
        "bio": None,
        "privacy_setting": "public",
        "profile_pic": None,
        "location": None,
    }

    def test_create_user(self, client):
        create_user_response = client.post(
            "/users",
            json={
                "email": f"{self.test_uuid}@test.com",
                "username": self.test_uuid,
                "password": "password",
                "name": "E2E Test",
            },
        )

        self.expected_user["id"] = create_user_response.json["id"]

        assert create_user_response.status_code == 200
        assert create_user_response.json == self.expected_user

    def test_get_user(self, client):
        get_user_response = client.get(f'/users/{self.expected_user["id"]}')

        assert get_user_response.status_code == 200
        assert get_user_response.json == self.expected_user

    def test_fixture_user(self, test_base_user):
        assert test_base_user["base_user"]["name"] == "E2E BASE USER"

    def test_update_user(self, client, test_base_user):
        updated_user = {
            "name": "Updated E2E Test",
            "bio": "I am a test",
        }
        update_user_response = client.patch(
            f'/users/{test_base_user["base_user"]["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
            json=updated_user,
        )
        expected_updated_user = {
            "id": test_base_user["base_user"]["id"],
            "email": test_base_user["base_user"]["email"],
            "username": test_base_user["base_user"]["username"],
            "name": "Updated E2E Test",
            "bio": "I am a test",
            "profile_pic": None,
            "privacy_setting": "public",
            "location": None,
        }

        assert update_user_response.status_code == 200
        assert update_user_response.json == expected_updated_user

    def test_follow_user(self, client, test_base_user):
        base_user = test_base_user["base_user"]
        follow_user_response = client.post(
            f'/users/{self.expected_user["id"]}/follow',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert follow_user_response.status_code == 200
        assert follow_user_response.json == {
            "followee_id": self.expected_user["id"],
            "follower_id": base_user["id"],
            "status": "accepted",
        }

    def test_get_followers(self, client, test_base_user):
        get_followers_response = client.get(
            f'/users/{self.expected_user["id"]}/followers',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert get_followers_response.status_code == 200
        assert get_followers_response.json == [
            {
                "id": test_base_user["base_user"]["id"],
                "username": test_base_user["base_user"]["username"],
                "name": "Updated E2E Test",
                "profile_pic": None,
            }
        ]

    def test_get_followings(self, client, test_base_user):
        get_followings_response = client.get(
            f'/users/{test_base_user["base_user"]["id"]}/following',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert get_followings_response.status_code == 200
        assert get_followings_response.json == [
            {
                "id": self.expected_user["id"],
                "username": self.expected_user["username"],
                "name": self.expected_user["name"],
                "profile_pic": None,
            }
        ]

    def test_unfollow_user(self, client, test_base_user):
        unfollow_user_response = client.post(
            f'/users/{self.expected_user["id"]}/unfollow',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert unfollow_user_response.status_code == 204

    def test_remove_follow(self, client, test_base_user):
        # second user follows base user
        client.post(
            f'/users/{test_base_user["base_user"]["id"]}/follow',
            headers={"Authorization": f'Bearer {test_base_user["second_token"]}'},
        )

        # base user removes second user as follower
        remove_follower_response = client.delete(
            f'/users/{test_base_user["second_user"]["id"]}/follower',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert remove_follower_response.status_code == 204

    def test_privacy_setting(self, client, test_base_user):
        # test sending follow request, listing follow requests, accepting follow request

        # base user tries to get private user profile posts
        get_private_profile_response = client.get(
            f'/profiles/{test_base_user["private_user"]["id"]}/workouts',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert get_private_profile_response.status_code == 403

        # base user sends follow request to private user
        follow_user_response = client.post(
            f'/users/{test_base_user["private_user"]["id"]}/follow',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert follow_user_response.status_code == 200
        assert follow_user_response.json == {
            "followee_id": test_base_user["private_user"]["id"],
            "follower_id": test_base_user["base_user"]["id"],
            "status": "pending",
        }

        # private user lists follow requests
        get_follow_requests_response = client.get(
            "/users/follow_requests",
            headers={"Authorization": f'Bearer {test_base_user["private_token"]}'},
        )
        assert get_follow_requests_response.status_code == 200
        assert get_follow_requests_response.json == [
            {
                "id": test_base_user["base_user"]["id"],
                "username": test_base_user["base_user"]["username"],
                "name": "Updated E2E Test",
                "profile_pic": None,
            }
        ]

        # private user accepts follow request
        accept_follow_request_response = client.put(
            f'/users/{test_base_user["base_user"]["id"]}/follower',
            headers={"Authorization": f'Bearer {test_base_user["private_token"]}'},
        )
        assert accept_follow_request_response.status_code == 200
        assert accept_follow_request_response.json == {
            "follower_id": test_base_user["base_user"]["id"],
            "followee_id": test_base_user["private_user"]["id"],
            "status": "accepted",
        }

        # base user gets private profile posts
        get_private_profile_response = client.get(
            f'/profiles/{test_base_user["private_user"]["id"]}/workouts',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert get_private_profile_response.status_code == 200
        assert get_private_profile_response.json == []
