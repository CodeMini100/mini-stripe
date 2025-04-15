import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import create_app
from config import load_config

# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------
@pytest.fixture(scope="module")
def client():
    """
    Fixture to provide a TestClient instance for the FastAPI app.
    """
    load_config()  # Load any config if necessary
    app = create_app()
    return TestClient(app)

# -------------------------------------------------------------------
# Tests for create_charge_endpoint
# -------------------------------------------------------------------
@pytest.mark.describe("POST /payments/create_charge - success case")
def test_create_charge_success(client):
    """
    Test successful charge creation using valid request data.
    Expect a 201 (or 200) response and a valid response body.
    """
    request_data = {
        "customer_id": "cust_123",
        "amount": 5000,
        "payment_method": "card_test"
    }

    with patch("payments.payments_service.create_charge") as mock_create_charge:
        # Mock return value for the service function
        mock_create_charge.return_value = {
            "charge_id": "chrg_123",
            "customer_id": "cust_123",
            "amount": 5000,
            "status": "succeeded"
        }

        response = client.post("/payments/create_charge", json=request_data)
        assert response.status_code in [200, 201], "Expected success status code"
        response_json = response.json()
        assert response_json["charge_id"] == "chrg_123"
        assert response_json["status"] == "succeeded"

@pytest.mark.describe("POST /payments/create_charge - error case (missing fields)")
def test_create_charge_missing_fields(client):
    """
    Test that the endpoint returns an error when
    required fields are missing (e.g., 'amount').
    """
    # customer_id present but 'amount' is missing
    request_data = {
        "customer_id": "cust_123",
        "payment_method": "card_test"
    }

    response = client.post("/payments/create_charge", json=request_data)
    # Expecting a validation error or similar
    assert response.status_code == 422, "Expected validation error status"

@pytest.mark.describe("POST /payments/create_charge - error case (invalid amount)")
def test_create_charge_invalid_amount(client):
    """
    Test that the endpoint returns an error
    when the amount is invalid (e.g., negative).
    """
    request_data = {
        "customer_id": "cust_123",
        "amount": -100,
        "payment_method": "card_test"
    }

    # Mocking the service to ensure it's not called with invalid data
    with patch("payments.payments_service.create_charge") as mock_create_charge:
        response = client.post("/payments/create_charge", json=request_data)
        assert response.status_code == 400, "Expected Bad Request status code"
        mock_create_charge.assert_not_called()

# -------------------------------------------------------------------
# Tests for refund_charge_endpoint
# -------------------------------------------------------------------
@pytest.mark.describe("POST /payments/refund_charge/{charge_id} - success case")
def test_refund_charge_success(client):
    """
    Test successful refund processing with a valid charge_id.
    """
    charge_id = "chrg_123"
    with patch("payments.payments_service.refund_charge") as mock_refund_charge:
        mock_refund_charge.return_value = {
            "charge_id": charge_id,
            "status": "refunded"
        }

        response = client.post(f"/payments/refund_charge/{charge_id}")
        assert response.status_code in [200, 201], "Expected success status code"
        response_json = response.json()
        assert response_json["status"] == "refunded"

@pytest.mark.describe("POST /payments/refund_charge/{charge_id} - error case (not found)")
def test_refund_charge_not_found(client):
    """
    Test that processing a refund for a non-existent charge
    returns an appropriate error response (404 or 400).
    """
    non_existent_charge_id = "chrg_invalid"
    with patch("payments.payments_service.refund_charge") as mock_refund_charge:
        # Simulate service raising an exception or returning None
        mock_refund_charge.side_effect = ValueError("Charge not found")

        response = client.post(f"/payments/refund_charge/{non_existent_charge_id}")
        assert response.status_code == 404, "Expected Not Found status code"

@pytest.mark.describe("POST /payments/refund_charge/{charge_id} - error case (already refunded)")
def test_refund_charge_already_refunded(client):
    """
    Test that the endpoint returns an appropriate error
    when attempting to refund an already refunded charge.
    """
    charge_id = "chrg_refunded"
    with patch("payments.payments_service.refund_charge") as mock_refund_charge:
        # Simulate service returning an error for a duplicate refund
        mock_refund_charge.side_effect = ValueError("Already refunded")

        response = client.post(f"/payments/refund_charge/{charge_id}")
        assert response.status_code == 400, "Expected Bad Request status code"