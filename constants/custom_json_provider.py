from datetime import time
from flask.json.provider import DefaultJSONProvider

import logging

logger = logging.getLogger()

class CustomJSONProvider(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)

    def default(self, obj):
        if isinstance(obj, time):
            return obj.isoformat()
        return super().default(obj)
