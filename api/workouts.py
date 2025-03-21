from datetime import datetime
from flask_classful import FlaskView, route
from flask import g, request
from middleware.token_required import token_required
from services.attendee_service import AttendeeService
from services.workout_service import WorkoutService


class WorkoutsView(FlaskView):
    route_base = "workouts"

    @route("/pending", methods=["GET"])
    @token_required
    def get_pending(self):
        page = request.args.get("page", 1, int)
        service_data = WorkoutService().get_pending_workouts(page)
        return service_data, 200

    @route("/upcoming", methods=["GET"])
    @token_required
    def get_upcoming(self):
        page = request.args.get("page", 1, int)
        date = datetime.strptime(request.args.get("date"), "%m/%d/%y")
        user_id = g.user_id
        service_data = WorkoutService().get_upcoming_workouts(
            user_id, date, "accepted", page
        )
        return service_data, 200

    @route("/invites", methods=["GET"])
    @token_required
    def get_invites(self):
        page = request.args.get("page", 1, int)
        date = datetime.strptime(request.args.get("date"), "%m/%d/%y")
        user_id = g.user_id
        service_data = WorkoutService().get_upcoming_workouts(
            user_id, date, "pending", page
        )
        return service_data, 200

    @route("", methods=["POST"])
    @token_required
    def create_workout(self):
        request_data = request.get_json()
        request_data["organizer_id"] = g.user_id
        service_data = WorkoutService().create_workout(request_data)
        return service_data.to_json(), 200

    @route("/<workout_id>", methods=["GET"])
    @token_required
    def get_workout(self, workout_id):
        service_data = WorkoutService().get_workout(workout_id)
        return service_data, 200

    @route("/<workout_id>", methods=["PATCH"])
    @token_required
    def update_workout(self, workout_id):
        request_data = request.get_json()
        service_data = WorkoutService().update_workout(workout_id, data=request_data)
        return service_data, 200

    @route("/<workout_id>", methods=["DELETE"])
    @token_required
    def delete_workout(self, workout_id):
        WorkoutService().delete_workout(workout_id)
        return "", 204

    @route("/<workout_id>/users", methods=["GET"])
    def list_workout_attendees(
        self, workout_id
    ):  # TODO: Add pagination - or not bc we need all attendees for EditWorkout screen
        service_data = AttendeeService().list_workout_attendees(workout_id)
        return [attendee for attendee in service_data], 200

    @route("/<workout_id>/accept", methods=["POST"])
    @token_required
    def accept_workout(self, workout_id):
        service_data = AttendeeService().accept_workout(workout_id, g.user_id)
        return service_data, 200

    @route("/<workout_id>/publish", methods=["POST"])
    @token_required
    def publish_workout(self, workout_id):
        service_data = WorkoutService().publish_workout(workout_id)
        return service_data, 200

    @route("/<workout_id>/reject", methods=["POST"])
    @token_required
    def reject_workout(self, workout_id):
        AttendeeService().delete_attendee(workout_id, g.user_id)
        return "", 204

    def serialize_attendee(self, attendee):
        return {
            "id": attendee.id,
            "username": attendee.username,
            "name": attendee.name,
            "profile_pic": attendee.profile_pic,
            "status": attendee.status,
        }
