from flask import request
from functools import wraps

from .api_utils import bad_request_error


def validate_request_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method in ['POST', 'PUT']:
            number_fields = ['id', 'value', 'monthyPrice', 'setupPrice', 'currency']

            # Verify if is a valid json
            data = request.json or {}
            if not data:
                raise bad_request_error('Request body must be a valid json')

            # PUT doesn't need id field on body
            if request.method == 'PUT':
                number_fields = number_fields[1:]

            # Verify missing fields
            missing_fields = [field for field in number_fields if field not in data]
            if missing_fields:
                raise bad_request_error(f'Missing fields: {missing_fields}')

        return f(*args, **kwargs)
    return wrapper
