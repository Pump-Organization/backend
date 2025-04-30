from db.models.attendee import AttendeeStatusEnum, AttendeeTypeEnum
from db.models.workout import WorkoutStatusEnum


class TestWorkoutsEndToEndTests:
    expected_workout = {
        "city": "San Francisco",
        "datetime": "2024-08-30T08:00:00",
        "endtime": "2024-08-30T09:00:00",
        "description": "I hope you like rowing...",
        "location": "Office Gym",
        "title": "Friday pull day",
        "intensity": None,
        "workout_pic": None,
        "status": WorkoutStatusEnum.pending.value,
    }

    def test_create_workout(self, client, test_base_user):
        create_workout_response = client.post(
            "/workouts",
            json={
                "city": "San Francisco",
                "datetime": "08/30/24 08:00",
                "endtime": "08/30/24 09:00",
                "description": "I hope you like rowing...",
                "location": "Office Gym",
                "title": "Friday pull day",
                "invitees": [test_base_user["second_user"]["id"]],
            },
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )

        self.expected_workout["id"] = create_workout_response.json["id"]

        assert create_workout_response.status_code == 200
        assert create_workout_response.json == self.expected_workout

    def test_get_workout(self, client, test_base_user):
        get_workout_response = client.get(
            f'/workouts/{self.expected_workout["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        get_expected_workout = self.expected_workout.copy()
        get_expected_workout["is_liked"] = False
        get_expected_workout["num_likes"] = 0
        get_expected_workout["num_comments"] = 0
        get_expected_workout["organizer_id"] = test_base_user["base_user"]["id"]
        get_expected_workout["organizer_username"] = test_base_user["base_user"][
            "username"
        ]
        get_expected_workout["routine"] = []
        get_expected_workout["organizer_pic"] = None
        get_expected_workout["attendees"] = [
            {
                "attendee_type": "organizer",
                "status": "accepted",
                "user_id": test_base_user["base_user"]["id"],
                "user_pic": None,
                "workout_id": get_expected_workout["id"],
            },
            {
                "attendee_type": "guest",
                "status": "pending",
                "user_id": test_base_user["second_user"]["id"],
                "user_pic": None,
                "workout_id": get_expected_workout["id"],
            },
        ]
        assert get_workout_response.status_code == 200
        assert get_workout_response.json == get_expected_workout

    def test_update_workout(self, client, test_base_user):
        updated_workout = {
            "city": "San Francisco",
            "datetime": "08/30/24 08:30",
            "endtime": "08/30/24 09:30",
            "description": "I hope you like rowing...",
            "location": "Office Gym",
            "title": "Updated Friday pull day",
        }
        update_workout_response = client.patch(
            f'/workouts/{self.expected_workout["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
            json=updated_workout,
        )
        expected_updated_workout = {
            "id": self.expected_workout["id"],
            "city": "San Francisco",
            "datetime": "2024-08-30T08:30:00",
            "endtime": "2024-08-30T09:30:00",
            "description": "I hope you like rowing...",
            "location": "Office Gym",
            "title": "Updated Friday pull day",
            "workout_pic": None,
            "intensity": None,
            "status": WorkoutStatusEnum.pending.value,
            "routine": [],
            "attendees": [
                {
                    "attendee_type": "organizer",
                    "status": "accepted",
                    "user_id": test_base_user["base_user"]["id"],
                    "user_pic": None,
                    "workout_id": self.expected_workout["id"],
                },
                {
                    "attendee_type": "guest",
                    "status": "pending",
                    "user_id": test_base_user["second_user"]["id"],
                    "user_pic": None,
                    "workout_id": self.expected_workout["id"],
                },
            ],
        }

        assert update_workout_response.status_code == 200
        assert update_workout_response.json == expected_updated_workout

    def test_list_workout_attendees(self, client, test_base_user):
        list_workout_attendees_response = client.get(
            f'/workouts/{self.expected_workout["id"]}/users'
        )

        assert list_workout_attendees_response.status_code == 200
        assert list_workout_attendees_response.json == [
            {
                "status": AttendeeStatusEnum.accepted.value,
                "user_id": test_base_user["base_user"]["id"],
                "username": test_base_user["base_user"]["username"],
                "user_pic": None,
                "attendee_type": AttendeeTypeEnum.organizer.value,
            },
            {
                "status": AttendeeStatusEnum.pending.value,
                "user_id": test_base_user["second_user"]["id"],
                "username": test_base_user["second_user"]["username"],
                "user_pic": None,
                "attendee_type": AttendeeTypeEnum.guest.value,
            },
        ]

    def test_accept_workout(self, client, test_base_user):
        accept_workout_response = client.post(
            f'/workouts/{self.expected_workout["id"]}/accept',
            headers={"Authorization": f'Bearer {test_base_user["second_token"]}'},
        )

        assert accept_workout_response.status_code == 200
        assert accept_workout_response.json == {
            "attendee_type": AttendeeTypeEnum.guest.value,
            "status": AttendeeStatusEnum.accepted.value,
            "user_id": test_base_user["second_user"]["id"],
            "workout_id": self.expected_workout["id"],
            "user_pic": None,
        }

    def test_reject_workout(self, client, test_base_user):
        reject_workout_response = client.post(
            f'/workouts/{self.expected_workout["id"]}/reject',
            headers={"Authorization": f'Bearer {test_base_user["second_token"]}'},
        )
        assert reject_workout_response.status_code == 204

        # check that the user is no longer in the list of attendees
        list_workout_attendees_response = client.get(
            f'/workouts/{self.expected_workout["id"]}/users'
        )

        assert list_workout_attendees_response.status_code == 200
        assert list_workout_attendees_response.json == [
            {
                "status": AttendeeStatusEnum.accepted.value,
                "attendee_type": AttendeeTypeEnum.organizer.value,
                "user_id": test_base_user["base_user"]["id"],
                "username": test_base_user["base_user"]["username"],
                "user_pic": None,
            }
        ]

    def test_publish_workout(self, client, test_base_user):
        publish_workout_response = client.post(
            f'/workouts/{self.expected_workout["id"]}/publish',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert publish_workout_response.status_code == 200
        assert publish_workout_response.json == {
            "id": self.expected_workout["id"],
            "city": "San Francisco",
            "datetime": "2024-08-30T08:30:00",
            "endtime": "2024-08-30T09:30:00",
            "description": "I hope you like rowing...",
            "location": "Office Gym",
            "title": "Updated Friday pull day",
            "workout_pic": None,
            "status": WorkoutStatusEnum.published.value,
            "intensity": None,
            "routine": [],
            "attendees": [
                {
                    "attendee_type": "organizer",
                    "status": "accepted",
                    "user_id": test_base_user["base_user"]["id"],
                    "user_pic": None,
                    "workout_id": self.expected_workout["id"],
                }
            ],
        }

    def test_delete_workout(self, client, test_base_user):
        delete_workout_response = client.delete(
            f'/workouts/{self.expected_workout["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert delete_workout_response.status_code == 204

        # check that the workout is no longer in the list of workouts
        get_workout_response = client.get(
            f'/workouts/{self.expected_workout["id"]}',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
        )
        assert get_workout_response.status_code == 404

    def test_report_workout(self, client, test_base_user, test_base_workout):
        report_workout_response = client.post(
            f'/workouts/{test_base_workout["id"]}/report',
            headers={"Authorization": f'Bearer {test_base_user["token"]}'},
            json={"reason": "Inappropriate content"},
        )

        assert report_workout_response.status_code == 200
        assert report_workout_response.json == {
            "message": "Reported successfully",
        }
