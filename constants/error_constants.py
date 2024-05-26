class AppError(Exception):
    def __init__(self):
        super().__init__()
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

CUSTOM_ERRORS = {AppError, NotFoundError, BadDataError, UnauthorizedError, ForbiddenError}
