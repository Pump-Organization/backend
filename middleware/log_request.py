import logging
import json
from flask import request


def log_request():
    log_data = {
        "method": request.method,
        "path": request.path,
    }
    try:
        if request.data:
            body = json.loads(request.data.decode("utf-8"))
            log_data["body"] = {k: v if k != "password" else "***" for k, v in body.items()}
    except (json.JSONDecodeError, UnicodeDecodeError):
        log_data["body"] = request.data.decode("utf-8", errors="replace")

    logging.debug(json.dumps(log_data))
