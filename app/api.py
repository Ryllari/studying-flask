import json

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort, HTTPException

from .api_utils import create_did_number, update_did_number
from .models import DIDNumber
from .paginator import paginate
from .validators import validate_request_data

bp = Blueprint('number', __name__)


@bp.app_errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@bp.route('/', methods=['GET', 'POST'])
@validate_request_data
def list_numbers():
    # Create a new DID Number
    if request.method == 'POST':
        created = create_did_number(request.json)
        return jsonify(created), 201

    # GET - List all DID Number
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except (TypeError, ValueError):
        abort(404)

    response_data = paginate(DIDNumber.query.order_by(DIDNumber.id.asc()), page=page, per_page=per_page)
    return jsonify(dict(response_data))


@bp.route('/<int:pk>/', methods=['GET', 'PUT', 'DELETE'])
@validate_request_data
def manage_number(pk):
    number = DIDNumber.query.get_or_404(pk)

    # Update a DID Number
    if request.method == "PUT":
        return jsonify(update_did_number(number, request.json))

    # Update a DID Number
    if request.method == "DELETE":
        number.delete()
        return {}, 204

    # GET - Retrieve a DID Number
    return jsonify(number.as_dict())
