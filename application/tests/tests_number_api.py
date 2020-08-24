from flask import url_for

from app.models import DIDNumber
from app.paginator import paginate
from app.utils import create_instance

from tests.base_tests import BaseTestAPI


class TestListNumbersAPI(BaseTestAPI):
    """
    This class tests number.list_numbers endpoint
    """
    def setUp(self):
        super().setUp()
        self.number_data = {
            "value": "+55 84 91234-432",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }

        # Create multi instances
        for i in range(30):
            self.number_data.update({"id": i})
            self.number_data.update({"value": self.number_data["value"] + f"{i}"})
            create_instance(self.number_data)

    # GET METHOD TESTS
    def test_list_did_number_with_no_auth_user_return_401(self):
        response = self.client.get(url_for('number.list_numbers'))

        self.assertEqual(response.status_code, 401)

    def test_list_did_number_with_data_return_200(self):
        response = self.client.get(url_for('number.list_numbers'), headers=self.token_header)

        data = paginate(DIDNumber.query.order_by(DIDNumber.id.asc()), page=1, per_page=20)
        self.assertEqual(response.json, data)
        self.assertEqual(response.status_code, 200)

    def test_list_did_number_with_data_and_page_queries_return_200(self):
        response = self.client.get(url_for('number.list_numbers', page=3, per_page=10), headers=self.token_header)

        data = paginate(DIDNumber.query.order_by(DIDNumber.id.asc()), page=3, per_page=10)
        self.assertEqual(response.json, data)
        self.assertEqual(response.status_code, 200)

    def test_list_did_number_with_invalid_page_number_return_404(self):
        response = self.client.get(url_for('number.list_numbers', page=100), headers=self.token_header)

        self.assertEqual(response.status_code, 404)

    def test_list_did_number_with_negative_page_number_return_404(self):
        response = self.client.get(url_for('number.list_numbers', page=-1), headers=self.token_header)

        self.assertEqual(response.status_code, 404)

    def test_list_did_number_with_str_page_number_return_404(self):
        response = self.client.get(url_for('number.list_numbers', page='aaa'), headers=self.token_header)

        self.assertEqual(response.status_code, 404)

    # POST METHOD TESTS
    def test_create_did_number_with_no_auth_user_return_401(self):
        self.number_data.update({"id": 31})
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data)

        self.assertEqual(response.status_code, 401)

    def test_create_did_number_without_data_return_400(self):
        self.number_data.update({"id": 31})
        response = self.client.post(url_for('number.list_numbers'), headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_create_did_number_with_id_missing_field_return_400(self):
        self.number_data.pop('id')
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data, headers=self.token_header)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['description'], 'Missing fields: [\'id\']')

    def test_create_did_number_with_invalid_id_return_400(self):
        self.number_data.update({"id": 'bla'})
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data, headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_create_did_number_with_invalid_monthyprice_return_400(self):
        self.number_data.update({"monthyPrice": 'bla'})
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data, headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_create_did_number_with_invalid_setupprice_return_400(self):
        self.number_data.update({"setupPrice": '-3'})
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data, headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_create_did_number_return_201(self):
        self.number_data.update({"id": 31})
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data, headers=self.token_header)
        number = DIDNumber.query.get(31)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, number.as_dict())

    def test_create_did_number_with_existing_return_400(self):
        self.number_data.update({"id": 1})
        response = self.client.post(url_for('number.list_numbers'), json=self.number_data, headers=self.token_header)

        self.assertEqual(response.status_code, 400)


class TestManageNumberAPI(BaseTestAPI):
    """
    This class tests number.manage_number endpoint
    """
    def setUp(self):
        super().setUp()
        self.number_data = {
            "id": 1,
            "value": "+55 84 91234-432",
            "monthyPrice": "0.03",
            "setupPrice": "3.40",
            "currency": "U$"
        }
        create_instance(self.number_data)

    # GET METHOD TESTS
    def test_retrieve_did_number_with_no_auth_user_return_401(self):
        response = self.client.get(url_for('number.manage_number', pk=1))

        self.assertEqual(response.status_code, 401)

    def test_retrieve_did_number_return_200(self):
        response = self.client.get(url_for('number.manage_number', pk=1), headers=self.token_header)
        number = DIDNumber.query.get(1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, number.as_dict())

    def test_retrieve_did_number_non_existing_return_404(self):
        response = self.client.get(url_for('number.manage_number', pk=100), headers=self.token_header)

        self.assertEqual(response.status_code, 404)

    # DELETE METHOD TESTS
    def test_delete_did_number_with_no_auth_user_return_401(self):
        response = self.client.delete(url_for('number.manage_number', pk=1))

        self.assertEqual(response.status_code, 401)

    def test_delete_did_number_return_204(self):
        response = self.client.delete(url_for('number.manage_number', pk=1), headers=self.token_header)

        self.assertEqual(response.status_code, 204)

    def test_delete_did_number_non_existing_return_404(self):
        response = self.client.delete(url_for('number.manage_number', pk=100), headers=self.token_header)

        self.assertEqual(response.status_code, 404)

    # PUT METHOD TESTS
    def test_update_did_number_with_no_auth_user_return_401(self):
        self.number_data.pop('id')
        response = self.client.put(url_for('number.manage_number', pk=1), json=self.number_data)

        self.assertEqual(response.status_code, 401)

    def test_update_did_number_without_data_return_400(self):
        response = self.client.put(url_for('number.manage_number', pk=1), headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_update_did_number_with_id_missing_field_return_200(self):
        self.number_data.pop('id')
        response = self.client.put(url_for('number.manage_number', pk=1), json=self.number_data,
                                   headers=self.token_header)

        self.assertEqual(response.status_code, 200)

    def test_update_did_number_with_id_and_value_missing_field_return_400(self):
        self.number_data.pop('id')
        self.number_data.pop('value')
        response = self.client.put(url_for('number.manage_number', pk=1), json=self.number_data,
                                   headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_update_did_number_with_invalid_monthyprice_return_400(self):
        self.number_data.pop('id')
        self.number_data.update({"monthyPrice": 'bla'})
        response = self.client.put(url_for('number.manage_number', pk=1), json=self.number_data,
                                   headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_update_did_number_with_invalid_setupprice_return_400(self):
        self.number_data.pop('id')
        self.number_data.update({"setupPrice": '-3'})
        response = self.client.put(url_for('number.manage_number', pk=1), json=self.number_data,
                                   headers=self.token_header)

        self.assertEqual(response.status_code, 400)

    def test_update_did_number_return_200(self):
        self.number_data.pop('id')
        response = self.client.put(url_for('number.manage_number', pk=1), json=self.number_data,
                                   headers=self.token_header)
        number = DIDNumber.query.get(1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, number.as_dict())

    def test_update_did_number_non_existing_return_404(self):
        self.number_data.pop('id')
        response = self.client.put(url_for('number.manage_number', pk=100), json=self.number_data,
                                   headers=self.token_header)

        self.assertEqual(response.status_code, 404)
