import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Relative import from the payments_router module
from ...payments.payments_router import router

# ------------------------------------------------------------------------
# Setup fixture to create a TestClient with the payments router included
# ------------------------------------------------------------------------
@pytest.fixture
def client():
    """
    Fixture that sets up a FastAPI app with the payments router and
    returns a TestClient instance for testing the endpoints.
    """
    app = FastAPI()
    app.include_router(router, prefix="/payments")
    yield TestClient(app)

# ------------------------------------------------------------------------
# Test: create_charge_endpoint - Successful Charge Creation
# ------------------------------------------------------------------------
def test_create_charge_success(client):
    """
    Test if 'create_charge_endpoint' successfully creates a charge
    when valid request data is provided.
    """
    request_data = {
        "amount": 1000,
        "currency": "USD",
        "customer_id": "cust_123",
        "description": "Test charge creation"
    }

    response = client.post("/payments/create_charge", json=request_data)
    assert response.status_code == 201, "Expected 201 Created for successful charge"
    response_data = response.json()
    assert "id" in response_data, "Response should contain the new charge ID"
    assert response_data["amount"] == request_data["amount"], "Charge amount should match request"
    assert response_data["currency"] == request_data["currency"], "Charge currency should match request"
    assert response_data["status"] == "created", "Charge status should be 'created'"

# ------------------------------------------------------------------------
# Test: create_charge_endpoint - Missing Data Error
# ------------------------------------------------------------------------
def test_create_charge_missing_data(client):
    """
    Test if 'create_charge_endpoint' returns an error when required
    data (e.g., amount) is missing.
    """
    invalid_request_data = {
        # "amount": 1000,  <-- Intentionally omitted
        "currency": "USD",
        "customer_id": "cust_123",
        "description": "Missing amount"
    }

    response = client.post("/payments/create_charge", json=invalid_request_data)
    assert response.status_code == 422, "Expected 422 Unprocessable Entity for missing required fields"

# ------------------------------------------------------------------------
# Test: create_charge_endpoint - Invalid Amount Error
# ------------------------------------------------------------------------
def test_create_charge_invalid_amount(client):
    """
    Test if 'create_charge_endpoint' returns an error when the amount is non-positive.
    """
    invalid_request_data = {
        "amount": -50,
        "currency": "USD",
        "customer_id": "cust_123",
        "description": "Invalid negative amount"
    }

    response = client.post("/payments/create_charge", json=invalid_request_data)
    assert response.status_code == 400, "Expected 400 Bad Request for invalid amount"
    assert "invalid amount" in response.text.lower(), "Error message should indicate invalid amount"

# ------------------------------------------------------------------------
# Test: refund_charge_endpoint - Successful Refund
# ------------------------------------------------------------------------
def test_refund_charge_success(client):
    """
    Test if 'refund_charge_endpoint' successfully processes
    a refund when the charge ID is valid.
    """
    # Mock or create a valid charge in the system. Here we simulate it by mocking.
    fake_charge_id = 123

    with patch("...payments.payments_router.refund_charge") as mock_refund:
        mock_refund.return_value = {"id": fake_charge_id, "status": "refunded"}

        response = client.post(f"/payments/refund/{fake_charge_id}")
        assert response.status_code == 200, "Expected 200 OK for a valid refund request"
        response_data = response.json()
        assert response_data["id"] == fake_charge_id, "Returned charge ID should match"
        assert response_data["status"] == "refunded", "Charge status should be 'refunded'"

# ------------------------------------------------------------------------
# Test: refund_charge_endpoint - Invalid Charge ID
# ------------------------------------------------------------------------
def test_refund_charge_invalid_id(client):
    """
    Test if 'refund_charge_endpoint' returns an error
    when the charge ID does not exist.
    """
    invalid_charge_id = 99999  # Assuming this ID does not exist

    response = client.post(f"/payments/refund/{invalid_charge_id}")
    assert response.status_code == 404, "Expected 404 Not Found when charge ID does not exist"
    assert "not found" in response.text.lower(), "Error message should indicate that the charge was not found"

# ------------------------------------------------------------------------
# Test: refund_charge_endpoint - Already Refunded
# ------------------------------------------------------------------------
def test_refund_charge_already_refunded(client):
    """
    Test if 'refund_charge_endpoint' returns an error
    when the charge is already refunded.
    """
    already_refunded_id = 456

    with patch("...payments.payments_router.refund_charge") as mock_refund:
        # Simulate a scenario where the charge is already refunded
        mock_refund.side_effect = ValueError("Charge is already refunded")

        response = client.post(f"/payments/refund/{already_refunded_id}")
        assert response.status_code == 400, "Expected 400 Bad Request if charge is already refunded"
        assert "already refunded" in response.text.lower(), "Error message should indicate already refunded status"