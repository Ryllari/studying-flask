import json
from datetime import timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import HTTPException

from .models import User
from .utils import bad_request_error
from .validators import validate_user_request_data

bp = Blueprint('user', __name__, url_prefix='/user')


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


@bp.route('/create/', methods=['POST'])
@validate_user_request_data
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if User.query.filter_by(username=request.json['username']).first() is not None:
        raise bad_request_error("User with this username already exists")

    user = User(username=username)
    user.hash_password(password)
    user.save()

    return jsonify(user.as_dict()), 201


@bp.route('/token/', methods=['POST'])
@validate_user_request_data
def create_token():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()

    if user and password and user.verify_password(password):
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=1)
        )

        return jsonify({'access_token': access_token})

    return jsonify({'message': 'Invalid credentials'}), 401
