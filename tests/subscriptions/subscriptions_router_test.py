import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Router import from the subscriptions module
from ...subscriptions.subscriptions_router import router

@pytest.fixture
def client():
    """
    Setup a FastAPI TestClient with the subscriptions router.
    Teardown happens automatically after tests complete.
    """
    app = FastAPI()
    app.include_router(router, prefix="/subscriptions")
    return TestClient(app)


@pytest.mark.parametrize("request_data, expected_status", [
    # Test valid subscription creation data
    ({"customer_id": 1, "plan_id": 2}, 200),
    # Test another valid scenario or variation if needed
    ({"customer_id": 2, "plan_id": 3}, 200),
])
def test_create_subscription_endpoint_success(client, request_data, expected_status):
    """
    Test successful subscription creation cases.
    """
    with patch("...subscriptions.subscriptions_router.create_subscription_in_db") as mock_create_subscription:
        # Mock the return value to mimic successful DB insertion
        mock_create_subscription.return_value = {"id": 123, **request_data, "status": "active"}

        response = client.post("/", json=request_data)
        assert response.status_code == expected_status
        data = response.json()
        assert "id" in data
        assert data["status"] == "active"
        mock_create_subscription.assert_called_once()


def test_create_subscription_endpoint_plan_not_found(client):
    """
    Test subscription creation failure when plan is not found.
    """
    request_data = {"customer_id": 1, "plan_id": 999}
    with patch("...subscriptions.subscriptions_router.create_subscription_in_db") as mock_create_subscription:
        # Simulate an exception or None return to indicate plan not found
        mock_create_subscription.side_effect = ValueError("Plan not found")

        response = client.post("/", json=request_data)
        assert response.status_code == 404
        assert "detail" in response.json()
        mock_create_subscription.assert_called_once()


def test_cancel_subscription_endpoint_success(client):
    """
    Test successful subscription cancellation.
    """
    subscription_id = 123
    with patch("...subscriptions.subscriptions_router.cancel_subscription_in_db") as mock_cancel_subscription:
        # Mock the return to show the subscription was successfully canceled
        mock_cancel_subscription.return_value = {"id": subscription_id, "status": "canceled"}

        response = client.delete(f"/{subscription_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == subscription_id
        assert data["status"] == "canceled"
        mock_cancel_subscription.assert_called_once_with(subscription_id)


def test_cancel_subscription_endpoint_not_found(client):
    """
    Test subscription cancellation failure when subscription is not found.
    """
    subscription_id = 999
    with patch("...subscriptions.subscriptions_router.cancel_subscription_in_db") as mock_cancel_subscription:
        # Simulate not found scenario
        mock_cancel_subscription.side_effect = ValueError("Subscription not found")

        response = client.delete(f"/{subscription_id}")
        assert response.status_code == 404
        assert "detail" in response.json()
        mock_cancel_subscription.assert_called_once_with(subscription_id)