import allure
import requests
import jsonschema
from .schemas.store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Place a new order for a pet")
    def test_post_new_order_in_store(self):
        with allure.step("Preparing data to create an order"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Sending a request to create an order"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)

        with allure.step("Check status code"):
            assert response.status_code == 200, "The response code did not match the expected one."


    @allure.title("Get order information by ID")
    def test_get_order_info_by_id(self, create_store):
        with allure.step("Getting ID of the created order"):
            store_id = create_store["id"]
        with allure.step("Sending a request to receive order information"):
            response = requests.get(url=f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Check status code"):
            assert response.status_code == 200, "The response code did not match the expected one"
            assert response.json()["id"] == store_id

    @allure.title("Delete purchase order by ID")
    def test_delete_order_by_id(self):

        with allure.step("Submitting a request to delete an order"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("Check status code"):
            assert response.status_code == 200, "The response code did not match the expected one"

        with allure.step("Submitting a deletion request"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Check status code"):
            assert response.status_code == 404, "The response code did not match the expected one"

    @allure.title("Get information about a non-existent order")
    def test_get_nonexistent_order(self):
        with allure.step("Sending a request to receive order information"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Check status code"):
            assert response.status_code == 404, "The response code did not match the expected one"

    @allure.title("Returns pet inventories by status")
    def test_get_store_inventory(self):
        with allure.step("Sending a request to receive order information"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Check status code"):
            assert response.status_code == 200, "The response code did not match the expected one"
            jsonschema.validate(response_json, STORE_SCHEMA)








