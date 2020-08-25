from datetime import timedelta
from unittest import TestCase

from flask_jwt_extended import create_access_token

from app import create_app
from app.models import User


class BaseTestAPI(TestCase):
    """
    Base Class to API Tests
    """
    def setUp(self):
        self.app = create_app(testing=True)
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

        # Create a base user
        self.user_username = 'manager'
        self.user_password = 'password1234'
        self.user = User(username=self.user_username)
        self.user.hash_password(self.user_password)
        self.user.save()

        # Base access token
        access_token = create_access_token(
            identity=self.user.id,
            expires_delta=timedelta(days=1)
        )
        self.token_header = {'Authorization': 'Bearer ' + access_token}

    def tearDown(self):
        self.app.db.drop_all()
