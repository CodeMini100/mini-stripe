import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy.orm import Session

# Import application factory and configuration
from main import create_app
from config import load_config


@pytest.fixture(scope="module")
def client():
    """
    Fixture to create a TestClient instance for the FastAPI application.
    """
    # Load any necessary config (if applicable)
    load_config()
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_db_session():
    """
    If testing requires a mocked database session, provide one here.
    Replace or extend with actual DB setup/teardown as needed.
    """
    # In real scenarios, you might mock or use a test DB session here
    # For demonstration, we return None or a mock object
    return None


def test_create_subscription_successful(client, mock_db_session):
    """
    Test that creating a subscription with valid data returns a successful response (201).
    Mocks the subscriptions_service.create_subscription to simulate DB interaction.
    """
    request_data = {
        "customer_id": "cust_123",
        "plan_id": "plan_pro"
    }

    with patch("subscriptions.subscriptions_service.create_subscription") as mock_create:
        # Simulate a successful subscription creation
        mock_create.return_value = {
            "subscription_id": "sub_456",
            "customer_id": "cust_123",
            "plan_id": "plan_pro",
            "status": "active"
        }
        response = client.post("/subscriptions", json=request_data)

    assert response.status_code == 201
    assert response.json()["subscription_id"] == "sub_456"
    assert response.json()["status"] == "active"


def test_create_subscription_invalid_data(client, mock_db_session):
    """
    Test that creating a subscription with invalid or missing data returns an error (422 or 400).
    """
    # Missing "plan_id"
    request_data = {
        "customer_id": "cust_123"
    }

    response = client.post("/subscriptions", json=request_data)

    # Expected to fail validation or return error
    assert response.status_code in (400, 422)
    assert "detail" in response.json()


def test_cancel_subscription_successful(client, mock_db_session):
    """
    Test that cancelling an existing subscription returns a successful response (200).
    Mocks the subscriptions_service.cancel_subscription to simulate DB interaction.
    """
    subscription_id = "sub_456"

    with patch("subscriptions.subscriptions_service.cancel_subscription") as mock_cancel:
        # Simulate a successful subscription cancellation
        mock_cancel.return_value = {
            "subscription_id": subscription_id,
            "status": "canceled"
        }
        response = client.post(f"/subscriptions/{subscription_id}/cancel")

    assert response.status_code == 200
    assert response.json()["subscription_id"] == subscription_id
    assert response.json()["status"] == "canceled"


def test_cancel_subscription_not_found(client, mock_db_session):
    """
    Test that cancelling a non-existent subscription returns a 404 response.
    """
    subscription_id = "sub_non_existent"

    # Simulate the service raising an exception or returning None for non-existent subscription
    with patch("subscriptions.subscriptions_service.cancel_subscription", side_effect=ValueError("Not found")):
        response = client.post(f"/subscriptions/{subscription_id}/cancel")

    assert response.status_code == 404
    assert "detail" in response.json()