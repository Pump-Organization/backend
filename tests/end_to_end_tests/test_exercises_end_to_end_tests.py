import json
from db.models.custom_user_exercise import ExerciseMetricTypeEnum
from pathlib import Path


class TestExercisesEndToEndTests:
    def test_crud_custom_exercise(self, client, test_base_user):
        # create a custom exercise
        create_exercise_response = client.post(
            "/custom_exercises",
            json={
                "name": "Custom Rowing",
                "equipment": "Rowing Machine",
                "muscle_group": "Back",
                "metric_type": ExerciseMetricTypeEnum.time_distance.value,
            },
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        expected_exercise = {
            "id": create_exercise_response.json["id"],
            "name": "Custom Rowing",
            "equipment": "Rowing Machine",
            "muscle_group": "Back",
            "metric_type": ExerciseMetricTypeEnum.time_distance.value,
        }

        assert create_exercise_response.status_code == 201
        assert create_exercise_response.json == expected_exercise

        # update the custom exercise
        update_exercise_response = client.patch(
            f'/custom_exercises/{create_exercise_response.json["id"]}',
            json={
                "name": "Updated Custom Rowing",
            },
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        expected_updated_exercise = {
            "id": create_exercise_response.json["id"],
            "name": "Updated Custom Rowing",
            "equipment": "Rowing Machine",
            "muscle_group": "Back",
            "metric_type": ExerciseMetricTypeEnum.time_distance.value,
        }

        assert update_exercise_response.status_code == 200
        assert update_exercise_response.json == expected_updated_exercise

        # list all exercises
        list_exercises_response = client.get(
            "/exercises",
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert list_exercises_response.status_code == 200
        assert len(list_exercises_response.json) == 102

        # delete the custom exercise
        delete_exercise_response = client.delete(
            f'/custom_exercises/{create_exercise_response.json["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert delete_exercise_response.status_code == 204

        # verify the exercise is deleted
        list_exercises_response_after_delete = client.get(
            "/exercises",
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        assert list_exercises_response_after_delete.status_code == 200
        assert len(list_exercises_response_after_delete.json) == 101
