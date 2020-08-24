from flask import url_for

from app.models import User

from tests.base_tests import BaseTestAPI


class TestCreateUserAPI(BaseTestAPI):
    """
    This class tests user.create_user endpoint
    """
    def setUp(self):
        super().setUp()
        self.data = {
            'username': 'new_user',
            'password': 'password123'
        }

    def test_create_user_without_data_return_400(self):
        response = self.client.post(url_for('user.create_user'))

        self.assertEqual(response.status_code, 400)

    def test_create_user_with_username_missing_field_return_400(self):
        self.data.pop('username')
        response = self.client.post(url_for('user.create_user'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_user_with_password_missing_field_return_400(self):
        self.data.pop('password')
        response = self.client.post(url_for('user.create_user'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_user_with_username_empty_return_400(self):
        self.data.update({'username': ''})
        response = self.client.post(url_for('user.create_user'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_user_with_password_empty_return_400(self):
        self.data.update({'password': ''})
        response = self.client.post(url_for('user.create_user'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_user_with_existing_username_return_400(self):
        # Creates to exists
        response = self.client.post(url_for('user.create_user'), json=self.data)
        self.assertEqual(response.status_code, 201)

        # Create again to error
        response = self.client.post(url_for('user.create_user'), json=self.data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_return_201(self):
        response = self.client.post(url_for('user.create_user'), json=self.data)
        user = User.query.filter_by(username=self.data['username']).first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, user.as_dict())


class TestCreateTokenAPI(BaseTestAPI):
    """
    This class tests user.create_token endpoint
    """
    def setUp(self):
        super().setUp()
        self.data = {
            "username": self.user_username,
            "password": self.user_password
        }

    def test_create_token_without_data_return_400(self):
        response = self.client.post(url_for('user.create_token'))

        self.assertEqual(response.status_code, 400)

    def test_create_token_with_username_missing_field_return_400(self):
        self.data.pop('username')
        response = self.client.post(url_for('user.create_token'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_token_with_password_missing_field_return_400(self):
        self.data.pop('password')
        response = self.client.post(url_for('user.create_token'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_token_with_username_empty_return_400(self):
        self.data.update({'username': ''})
        response = self.client.post(url_for('user.create_token'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_token_with_password_empty_return_400(self):
        self.data.update({'password': ''})
        response = self.client.post(url_for('user.create_token'), json=self.data)

        self.assertEqual(response.status_code, 400)

    def test_create_token_with_invalid_password_401(self):
        self.data.update({'password': 'bjas'})
        response = self.client.post(url_for('user.create_token'), json=self.data)

        self.assertEqual(response.status_code, 401)

    def test_create_token_return_200(self):
        response = self.client.post(url_for('user.create_token'), json=self.data)

        self.assertEqual(response.status_code, 200)
