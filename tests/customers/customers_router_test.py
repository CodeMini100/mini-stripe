import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import create_app


@pytest.fixture
def client():
    """
    Fixture to create a TestClient instance of the FastAPI app.
    """
    app = create_app()
    return TestClient(app)


@pytest.mark.describe("create_customer_endpoint tests")
class TestCreateCustomerEndpoint:

    @pytest.mark.it("should successfully create a new customer when valid data is provided")
    @patch("customers.customers_service.create_customer")
    def test_create_customer_success(self, mock_create_customer, client):
        # Arrange: mock the service layer to return a mocked customer object
        mock_create_customer.return_value = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "payment_info": "card_123"
        }

        # Act: send a POST request with valid JSON
        response = client.post("/customers", json={
            "name": "John Doe",
            "email": "john@example.com",
            "payment_info": "card_123"
        })

        # Assert: check the status code and response body
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        mock_create_customer.assert_called_once_with(
            "John Doe",
            "john@example.com",
            "card_123"
        )

    @pytest.mark.it("should return a validation error (422) when required fields are missing")
    @patch("customers.customers_service.create_customer")
    def test_create_customer_missing_fields(self, mock_create_customer, client):
        # Arrange: do not configure the mock to return anything because it shouldn't be called
        # Act: send a POST request with missing fields
        response = client.post("/customers", json={"name": "OnlyNameProvided"})

        # Assert: FastAPI should return a 422 for validation failure
        assert response.status_code == 422
        mock_create_customer.assert_not_called()

    @pytest.mark.it("should handle internal service errors gracefully (e.g., return 500)")
    @patch("customers.customers_service.create_customer", side_effect=Exception("Service error"))
    def test_create_customer_internal_error(self, mock_create_customer, client):
        # Act: send a valid POST request
        response = client.post("/customers", json={
            "name": "John Doe",
            "email": "john@example.com",
            "payment_info": "card_123"
        })

        # Assert: check the status code for internal server error or custom error handling
        assert response.status_code == 500
        assert "Service error" in response.text


@pytest.mark.describe("get_customer_endpoint tests")
class TestGetCustomerEndpoint:

    @pytest.mark.it("should return customer details when the customer exists")
    @patch("customers.customers_service.fetch_customer")
    def test_get_customer_success(self, mock_fetch_customer, client):
        # Arrange: mock the service layer to return a mocked customer object
        mock_fetch_customer.return_value = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com"
        }

        # Act: send a GET request to retrieve the customer
        response = client.get("/customers/1")

        # Assert: check that the response is successful and data matches
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        mock_fetch_customer.assert_called_once_with(1)

    @pytest.mark.it("should return 404 when the customer does not exist")
    @patch("customers.customers_service.fetch_customer", return_value=None)
    def test_get_customer_not_found(self, mock_fetch_customer, client):
        # Act: send a GET request with an ID that doesn't exist
        response = client.get("/customers/999")

        # Assert: check that a 404 is returned for non-existent customer
        assert response.status_code == 404
        mock_fetch_customer.assert_called_once_with(999)

    @pytest.mark.it("should handle invalid customer ID formats gracefully")
    def test_get_customer_invalid_id(self, client):
        # Act: pass a non-integer ID, expecting FastAPI's validation to fail (422)
        response = client.get("/customers/abc")

        # Assert: check that it fails validation
        assert response.status_code == 422