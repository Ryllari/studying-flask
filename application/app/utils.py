from werkzeug.exceptions import HTTPException

from .models import DIDNumber


def create_instance(data):
    if DIDNumber.query.filter_by(id=int(data["id"])).first():
        raise bad_request_error("DID Number with this id already exists")
    number = DIDNumber(
        id=data["id"],
        value=data["value"],
        monthyPrice=data["monthyPrice"],
        setupPrice=data["setupPrice"],
        currency=data["currency"]
    )
    number.save()

    return number.as_dict()


def update_instance(number, data):
    number.value = data.get("value", number.value)
    number.monthyPrice = data.get("monthyPrice", number.monthyPrice)
    number.setupPrice = data.get("setupPrice", number.setupPrice)
    number.currency = data.get("currency", number.currency)
    number.save()

    return number.as_dict()


def bad_request_error(description):
    error = HTTPException(description=description)
    error.code = 400
    return error
