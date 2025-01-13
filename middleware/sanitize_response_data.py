from flask import jsonify
from html_sanitizer import Sanitizer


# create a sanitizer instance
sanitizer = Sanitizer({
    'tags': ['b', 'i', 'u', 'strong', 'em', 'p', 'br', 'ul', 'ol', 'li', 'pre'],  # No allowed tags
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


# DONT NEED RIGHT NOW, frontend handles xss, but may be useful if we offer public api
def sanitize_json_response(response):
    # Only modify JSON responses
    if response.content_type == 'application/json':
        response_data = response.get_json()
        sanitized_data = sanitize_input(response_data)
        response.set_data(jsonify(sanitized_data).get_data())

    return response
