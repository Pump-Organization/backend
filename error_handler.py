import traceback
import logging
from constants.error_constants import (
    AppError,
    BadDataError,
    NotFoundError,
)
from sqlalchemy.exc import IntegrityError, DataError
from werkzeug.exceptions import NotFound

logger = logging.getLogger()


def handle_app_error(error):
    if isinstance(error, NotFound):
        error = NotFoundError
    elif type(error) in (IntegrityError, DataError, LookupError):
        error = BadDataError
    elif not isinstance(error, AppError):
        return handle_unexpected_error(error)

    return {"error": error.message}, error.status_code


def handle_unexpected_error(error):
    logger.critical(traceback.format_exc())
    return {"error": "unexpected error"}, 500
