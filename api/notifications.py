from flask_classful import FlaskView, route
from flask import g, request
from middleware.token_required import token_required
from services.dynamodb_services.notification_service import NotificationService


class NotificationsView(FlaskView):
    route_base = "notifications"

    @route("", methods=["GET"])
    @token_required
    def list_notifications(self):
        limit = request.args.get("limit", 10, int)
        last_evaluated_key = request.args.get("last_evaluated_key", None)
        notifications, last_evaluated_key = NotificationService().list_notifications(
            g.user_id.hex, limit, last_evaluated_key
        )
        if notifications:
            # mark the latest notification as viewed
            NotificationService().mark_notification_viewed(
                g.user_id.hex, notifications[0]["SK"]
            )

        return {
            "notifications": notifications,
            "last_evaluated_key": last_evaluated_key,
            "user_hex": g.user_id.hex,
        }, 200

    @route("/unviewed", methods=["GET"])
    @token_required
    def has_unviewed_notifications(self):
        has_unviewed = NotificationService().has_unviewed_notifications(g.user_id.hex)
        return {"has_unviewed": has_unviewed}, 200
