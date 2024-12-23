from flask import request
from constants.error_constants import BadDataError
from html_sanitizer import Sanitizer

# Create a sanitizer instance
sanitizer = Sanitizer({
    'tags': ['fake_nonexistent_tag'],  # No allowed tags
    'attributes': {},  # No allowed attributes
    'empty': set(),
    'separate': set(),
    'keep_typographic_whitespace': True,
})


def sanitize_input(data):
    if isinstance(data, dict):
        return {key: (sanitize_input(value) if key != 'password' else value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        return sanitizer.sanitize(data)
    else:
        return data
    
def sanitize_request_data():
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.get_json(silent=True):
            if request.json != sanitize_input(request.json):
                raise BadDataError
        if request.form:
            if request.form != sanitize_input(request.form):
                raise BadDataError
    if request.args:
        if request.args.to_dict() != sanitize_input(request.args.to_dict()):
            raise BadDataError
