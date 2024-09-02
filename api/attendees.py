from flask_classful import FlaskView, route
from flask import request
from middleware.token_required import token_required
from services.attendee_service import AttendeeService

class AttendeesView(FlaskView):
    route_base = 'attendees'

    @route('', methods=['POST'])
    @token_required
    def create_attendee(self):
        request_data = request.get_json()
        service_data = AttendeeService().create_attendee(request_data)
        return service_data.to_json(), 200
    
    @route('/<attendee_id>', methods=['GET'])
    def get_attendee(self, attendee_id):
        service_data = AttendeeService().get_attendee(attendee_id)
        return service_data.to_json(), 200

    @route('/<attendee_id>', methods=['PATCH'])
    @token_required
    def update_attendee(self, attendee_id):
        request_data = request.get_json()
        service_data = AttendeeService().update_attendee(attendee_id, data=request_data)
        return service_data.to_json(), 200

    @route('/<attendee_id>', methods=['DELETE'])
    @token_required
    def delete_attendee(self, attendee_id):
        AttendeeService().delete_attendee(attendee_id)
        return '', 204
