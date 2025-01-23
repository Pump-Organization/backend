class TestCommentsEndToEndTests:
    def test_crud_comment(self, client, test_base_user, test_base_workout):
        create_comment_response = client.post(
            f"comments",
            json={
                "workout_id": test_base_workout["id"],
                "content": "Great workout!",
            },
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        expected_comment = {
            "id": create_comment_response.json["id"],
            "user_id": test_base_user["base_user"]["id"],
            "user_username": test_base_user["base_user"]["username"],
            "user_pic": None,
            "workout_id": test_base_workout["id"],
            "content": "Great workout!",
        }

        assert create_comment_response.status_code == 200
        assert create_comment_response.json == expected_comment

        # Test getting comments for a post
        get_comments_response = client.get(
            f'comments/{test_base_workout["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        expected_comment = {
            "id": get_comments_response.json[0]["id"],
            "user_username": test_base_user["base_user"]["username"],
            "user_pic": None,
            "user_id": test_base_user["base_user"]["id"],
            "workout_id": test_base_workout["id"],
            "content": "Great workout!",
        }

        assert get_comments_response.status_code == 200
        assert get_comments_response.json == [expected_comment]

        # Test getting number of comments
        get_num_comments_response = client.get(
            f'comments/{test_base_workout["id"]}/num_comments',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert get_num_comments_response.status_code == 200
        assert get_num_comments_response.json == {"num_comments": 1}

        # Test deleting a comment
        delete_comment_response = client.delete(
            f'comments/{create_comment_response.json["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert delete_comment_response.status_code == 204
