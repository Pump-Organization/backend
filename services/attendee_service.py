import logging
import uuid
import traceback
from flask import g
from db.models.attendee import Attendee, AttendeeStatusEnum, AttendeeTypeEnum
from constants.error_constants import ForbiddenError
from services.service import Service
from services.user_service import UserService
from services.event_emitter_service import EventEmitterService


class AttendeeService(Service):
    def __init__(self) -> None:
        super().__init__(Attendee)

    def create_attendee(
        self, data, status=AttendeeStatusEnum.pending, organizer_id=None
    ):
        if g.get("blocked_users") and data.get("user_id") in g.blocked_users:
            raise ForbiddenError

        if organizer_id is None:
            organizer_id = self.get_workout_organizer(data.get("workout_id"))

        if g.user_id != organizer_id:
            raise ForbiddenError

        attendee = Attendee(
            user_id=data.get("user_id"),
            workout_id=data.get("workout_id"),
            attendee_type=data.get("attendee_type", AttendeeTypeEnum.guest),
            status=status,
        )
        response: Attendee = self.add_data(attendee)

        try:
            organizer = UserService().get_user(organizer_id)
            EventEmitterService().emit_event(
                {
                    "name": "INVITE-CREATED",
                    "data": {
                        "created_at": str(response.created_at),
                        "target_id": data.get("user_id"),
                        "subject_id": organizer_id.hex,
                        "subject_username": organizer.username,
                        "related_objects": [
                            {"type": "workout", "id": data.get("workout_id")}
                        ],
                    },
                }
            )
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return response

    def get_attendee(self, workout_id, user_id):
        attendee = (
            self.session.query(Attendee)
            .filter(Attendee.workout_id == workout_id, Attendee.user_id == user_id)
            .one()
        )
        return attendee

    def update_attendee(self, user_id, workout_id, data):
        attendee = self.get_attendee(workout_id, user_id)
        if attendee.user_id != g.user_id:
            raise ForbiddenError
        for key, value in data.items():
            setattr(attendee, key, value)
        self.session.commit()
        return attendee

    def delete_attendee(self, workout_id, user_id):
        attendee = (
            self.session.query(Attendee)
            .filter(Attendee.workout_id == workout_id, Attendee.user_id == user_id)
            .first()
        )
        if not attendee:
            return
        organizer_id = self.get_workout_organizer(workout_id)
        if g.user_id != attendee.user_id and g.user_id != organizer_id:
            raise ForbiddenError
        self.session.delete(attendee)
        self.session.commit()

        try:
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
            EventEmitterService().emit_event(
                {
                    "name": "INVITE-DELETED",
                    "data": {
                        "target_id": user_id.hex,
                        "subject_id": g.user_id.hex,
                        "created_at": str(attendee.created_at),
                    },
                }
            )
        except Exception:
            logging.critical("### Error emitting event")
            logging.critical(traceback.format_exc())

        return

    def list_workout_attendees(
        self, workout_id
    ):  # TODO: add pagination - or not bc we need all attendees for EditWorkout screen
        attendees = Attendee.query.filter_by(workout_id=workout_id).all()
        data = [attendee.to_full_user() for attendee in attendees]
        return data

    def get_workout_organizer(self, workout_id):
        organizer = (
            self.session.query(Attendee)
            .filter(
                Attendee.workout_id == workout_id,
                Attendee.attendee_type == AttendeeTypeEnum.organizer,
            )
            .first()
        )
        return organizer.user_id if organizer else None

    def accept_workout(self, workout_id, user_id):
        attendee = (
            self.session.query(Attendee)
            .filter(Attendee.workout_id == workout_id, Attendee.user_id == user_id)
            .first()
        )

        attendee.status = AttendeeStatusEnum.accepted
        self.session.commit()
        return attendee.to_json()

    def batch_create_attendees(self, workout_id: uuid.UUID, user_ids: list[uuid.UUID]):
        if g.user_id != self.get_workout_organizer(workout_id):
            raise ForbiddenError

        attendees = []
        for user_id in user_ids:
            try:
                self.create_attendee(
                    {
                        "workout_id": workout_id,
                        "user_id": user_id,
                        "attendee_type": AttendeeTypeEnum.guest,
                    }
                )
            except Exception as e:
                logging.error(f"Error creating attendee: {e}")
                traceback.print_exc()
                continue
            attendees.append(user_id)

        return attendees

    def batch_delete_attendees(self, workout_id: uuid.UUID, user_ids: list[uuid.UUID]):
        if g.user_id != self.get_workout_organizer(workout_id):
            raise ForbiddenError

        for user_id in user_ids:
            try:
                self.delete_attendee(workout_id, user_id)
            except Exception as e:
                logging.error(f"Error deleting attendee: {e}")
                traceback.print_exc()
                continue

        return
