import pytest

from main.helpers import generate_token
from main.schemas.item import ItemSchema
from tests.helpers import create_authorizaton_headers
from tests.setup_db import generate_users, generate_items, generate_categories


class TestPutItem:
    def _setup(self):
        self.users = generate_users()
        self.categories = generate_categories()
        self.items = generate_items()
        self.access_token = generate_token(self.users[0]["id"])
        self.put_item = {"name": "lamp2",
                         "description": "Slightly better lamp",
                         "category_id": self.categories[0]["id"]}

    def test_put_item_successfully(self, client):
        self._setup()
        response, json_response = put_item(client, item_id=self.items[0]["id"], data=self.put_item,
                                           access_token=self.access_token)

        assert response.status_code == 201, "Successful call should return 201 status code"
        assert ItemSchema().validate(json_response) == {}, "Validation should return empty error object"

    @pytest.mark.parametrize("item_id, data", [
        (1, {"description": "Slightly better lamp", "category_id": 1}),  # Missing name
        (1, {"name": "lamp2", "category_id": 1}),  # Missing description
        (1, {"name": "lamp2", "description": "Slightly better lamp"}),  # Missing category_id
        (1, {"name": 1231232, "description": "Slightly better lamp", "category_id": 1}),  # Name is not string
        (1, {"name": "lamp2", "description": 123123, "category_id": 1}),  # Description is not string
        (1, {"name": "lamp2", 'a' * 100: "Slightly better lamp", "category_id": "efwef"}),  # Category_id is not int
    ])
    def test_put_item_fail_with_invalid_request_data(self, client, item_id, data):
        self._setup()
        response, json_response = put_item(client, item_id=self.items[0]["id"], data=data,
                                           access_token=self.access_token)

        assert response.status_code == 400, "Invalid request data should return 400 status code"
        assert json_response["message"] == "Invalid request data."
        assert json_response["error"] != {}

    def test_put_item_fail_with_invalid_token(self, client):
        self._setup()
        response, json_response = put_item(client, item_id=1, data=self.put_item)

        assert response.status_code == 400, "Invalid credential call should return 401 status code"
        assert json_response["message"] == "Missing token. Please sign in first to perform this action."
        assert json_response["error"] == {}

    def test_put_item_fail_with_invalid_user(self, client):
        self._setup()
        access_token = generate_token(self.users[1])
        response, json_response = put_item(client, item_id=self.items[0]["id"], data=self.put_item,
                                           access_token=access_token)

        assert response.status_code == 403, "Forbiden call should return 403 status code"
        assert json_response["message"] == "You are not allowed to edit this item."
        assert json_response["error"] == {}

    def test_put_item_fail_with_not_exist_item(self, client):
        self._setup()
        response, json_response = put_item(client, item_id=100, data=self.put_item, access_token=self.access_token)

        assert response.status_code == 404, "Not found error should return 404 status code"
        assert json_response["message"] == "Item with id 100 does not exist."
        assert json_response["error"] == {}


def put_item(client, item_id, data, access_token=None):
    response = client.put(f"/items/{item_id}", headers=create_authorizaton_headers(access_token), json=data)
    json_response = response.get_json()

    return response, json_response
