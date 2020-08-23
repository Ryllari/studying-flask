from decimal import Decimal

from flask import request
from functools import wraps

from .utils import bad_request_error


def validate_number_request_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
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
            if missing_fields and request.method != 'PATCH':
                raise bad_request_error(f'Missing fields: {missing_fields}')

            # Verify data format
            try:
                int(data.get("id", 0))
                monthy = Decimal(data.get('monthyPrice', '0.00'))
                setup = Decimal(data.get('setupPrice', '0.00'))
                if any(t < 0 for t in [monthy, setup]):
                    raise
            except Exception as e:
                raise bad_request_error('Invalid data format')

        return f(*args, **kwargs)
    return wrapper
