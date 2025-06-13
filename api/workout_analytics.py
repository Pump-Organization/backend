from flask_classful import FlaskView, route
from middleware.token_required import token_required
from services.workout_service import WorkoutService


class WorkoutAnalyticsView(FlaskView):
    route_base = "workout_analytics"

    @route("", methods=["GET"])
    @token_required
    def get_workout_analytics(self):
        """
        Get workout analytics for the user.
        """
        service_data = WorkoutService().get_workout_analytics()
        return service_data, 200
