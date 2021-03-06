import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import abort, HTTPException

from .utils import create_instance, update_instance
from .models import DIDNumber
from .paginator import paginate
from .validators import validate_number_request_data

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
@jwt_required
@validate_number_request_data
def list_numbers():
    # Create a new DID Number on DB
    if request.method == 'POST':
        created = create_instance(request.json)
        return jsonify(created), 201

    # GET - List all DID Number on DB
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except (TypeError, ValueError):
        abort(404)

    response_data = paginate(DIDNumber.query.order_by(DIDNumber.id.asc()), page=page, per_page=per_page)
    return jsonify(dict(response_data))


@bp.route('/<int:pk>/', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@jwt_required
@validate_number_request_data
def manage_number(pk):
    number = DIDNumber.query.get_or_404(pk)

    # PUT/PATCH - Update a DID Number on DB
    if request.method in ["PUT", "PATCH"]:
        return jsonify(update_instance(number, request.json))

    # DELETE - Delete a DID Number on DB
    if request.method == "DELETE":
        number.delete()
        return {}, 204

    # GET - Retrieve a DID Number
    return jsonify(number.as_dict())
