import os

try:
    exec(f"from settings.{os.environ.get('ENVIRONMENT', 'local')} import *")
except:  # noqa
    from settings.local import *  # noqa
