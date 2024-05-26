from html_sanitizer import Sanitizer

# Create a sanitizer instance
sanitizer = Sanitizer({
    'tags': ['fake_nonexistent_tag'],  # No allowed tags
    'attributes': {},  # No allowed attributes
    'empty': set(),
    'separate': set()
})

def sanitize_input(data):
    if isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        return sanitizer.sanitize(data)
    else:
        return data
    