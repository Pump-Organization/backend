class TestSearchEndToEndTests:
    def test_search_users(self, client, test_base_user):
        search_users_response = client.get(
            f'/search?q={test_base_user["base_user"]["username"][:-1]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert search_users_response.status_code == 200
        assert sorted(search_users_response.json, key=lambda x: x["id"]) == sorted(
            [
                {
                    "id": test_base_user["base_user"]["id"],
                    "username": test_base_user["base_user"]["username"],
                    "name": test_base_user["base_user"]["name"],
                    "profile_pic": None,
                    "follow_status": "no",
                    "is_following": False,
                },
                {
                    "id": test_base_user["second_user"]["id"],
                    "username": test_base_user["second_user"]["username"],
                    "name": test_base_user["second_user"]["name"],
                    "profile_pic": None,
                    "follow_status": "no",
                    "is_following": False,
                },
                {
                    "id": test_base_user["private_user"]["id"],
                    "username": test_base_user["private_user"]["username"],
                    "name": test_base_user["private_user"]["name"],
                    "profile_pic": None,
                    "follow_status": "no",
                    "is_following": False,
                },
            ],
            key=lambda x: x["id"],
        )
