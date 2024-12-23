import logging
import json
from flask import request

def log_request():
    log_data = {
        "method": request.method,
        "path": request.path,
    }
    if request.json:
        log_data["body"] = {k: v if k != "password" else "***" for k, v in request.json.items()}
    
    logging.debug(json.dumps(log_data))
