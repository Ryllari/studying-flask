from flask import Flask
from flask_migrate import Migrate

from .models import config_db


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config_db(app)
    Migrate(app, app.db)

    from app import api
    app.register_blueprint(api.bp)

    return app
