class AppError(Exception):
    def __init__(self, message=None):
        super().__init__()
        if message is not None:
            self.message = message

    status_code = 500
    message = "internal server error"


class NotFoundError(AppError):
    status_code = 404
    message = "not found"


class BadDataError(AppError):
    status_code = 400
    message = "bad data"


class UnauthorizedError(AppError):
    status_code = 401
    message = "unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    message = "forbidden"


class ConflictError(AppError):
    status_code = 409
    message = "conflict"


CUSTOM_ERRORS = {
    AppError,
    NotFoundError,
    BadDataError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
}
