import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .models import config_db


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI", 'postgresql://postgres:postgres@db:5432/api_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'blabla'

    config_db(app)
    Migrate(app, app.db)

    JWTManager(app)

    # Routes
    from . import number_api, user_api
    app.register_blueprint(number_api.bp)
    app.register_blueprint(user_api.bp)

    return app
