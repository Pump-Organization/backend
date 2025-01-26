from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.attendee_service import AttendeeService


class AttendeesView(FlaskView):
    route_base = "attendees"

    @route("", methods=["POST"])
    @token_required
    def create_attendee(self):
        request_data = request.get_json()
        service_data = AttendeeService().create_attendee(request_data)
        return service_data.to_json(), 200
