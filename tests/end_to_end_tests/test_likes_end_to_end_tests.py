class TestLikesEndToEndTests:
    def test_create_like(self, client, test_base_user, test_base_workout):
        expected_like = {
            "user_id": test_base_user["base_user"]["id"],
            "workout_id": test_base_workout["id"],
        }

        create_like_response = client.post(f'likes', json={'workout_id': test_base_workout["id"]},
                                           headers={'Authorization': f'Bearer {test_base_user["token"]}'})
        assert create_like_response.status_code == 200
        assert create_like_response.json == expected_like

    def test_get_likes(self, client, test_base_user, test_base_workout):
        expected_like = {
            "user_id": test_base_user["base_user"]["id"],
            "workout_id": test_base_workout["id"],
        }

        get_likes_response = client.get(f'likes/{test_base_workout["id"]}',
                                       headers={'Authorization': f'Bearer {test_base_user["token"]}'})
        assert get_likes_response.status_code == 200
        assert get_likes_response.json == [expected_like]

    def test_get_num_likes(self, client, test_base_user, test_base_workout):
        get_num_likes_response = client.get(f'likes/{test_base_workout["id"]}/num_likes',
                                           headers={'Authorization': f'Bearer {test_base_user["token"]}'})
        assert get_num_likes_response.status_code == 200
        assert get_num_likes_response.json == {"num_likes": 1}
