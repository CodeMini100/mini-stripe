import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Relative imports from the project structure
from ...subscriptions.subscriptions_service import (
    create_subscription,
    cancel_subscription,
    generate_invoice
)
from ...models import Subscription, Invoice

@pytest.fixture
def mock_session():
    """
    Fixture to provide a mocked database session.
    """
    session = MagicMock(spec=Session)
    yield session

# --------------------------
# CREATE SUBSCRIPTION TESTS
# --------------------------

@pytest.mark.parametrize("customer_id, plan_id", [(1, 10), (2, 20)])
def test_create_subscription_success(mock_session, customer_id, plan_id):
    """
    Test that create_subscription successfully creates a subscription
    when valid customer and plan IDs are provided.
    """
    subscription_mock = MagicMock(spec=Subscription)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    with patch("...subscriptions.subscriptions_service.Subscription", return_value=subscription_mock):
        result = create_subscription(customer_id, plan_id)

    # Assert that a subscription-like object is returned,
    # and that the database session methods were called.
    assert result == subscription_mock
    mock_session.add.assert_called_once_with(subscription_mock)
    mock_session.commit.assert_called_once()

def test_create_subscription_invalid_input(mock_session):
    """
    Test that create_subscription raises an error or handles invalid inputs
    (e.g., invalid customer/plan IDs).
    """
    with pytest.raises(ValueError):
        create_subscription(None, None)

# --------------------------
# CANCEL SUBSCRIPTION TESTS
# --------------------------

def test_cancel_subscription_success(mock_session):
    """
    Test that cancel_subscription successfully cancels an existing subscription.
    """
    subscription_mock = MagicMock(spec=Subscription)
    subscription_mock.is_active = True

    mock_session.query.return_value.get.return_value = subscription_mock
    mock_session.commit.return_value = None

    cancel_subscription(1)  # Cancel subscription with ID=1

    # Assert state changes for subscription cancellation
    assert subscription_mock.is_active is False
    mock_session.commit.assert_called_once()

def test_cancel_subscription_not_found(mock_session):
    """
    Test that cancel_subscription handles the case where the subscription
    ID does not exist in the database.
    """
    mock_session.query.return_value.get.return_value = None

    with pytest.raises(ValueError, match="Subscription not found"):
        cancel_subscription(999)

# --------------------------
# GENERATE INVOICE TESTS
# --------------------------

def test_generate_invoice_success(mock_session):
    """
    Test that generate_invoice creates an invoice for the provided subscription ID.
    """
    subscription_mock = MagicMock(spec=Subscription)
    subscription_mock.id = 1
    mock_session.query.return_value.get.return_value = subscription_mock
    mock_session.commit.return_value = None

    invoice_mock = MagicMock(spec=Invoice)
    with patch("...subscriptions.subscriptions_service.Invoice", return_value=invoice_mock):
        result = generate_invoice(subscription_mock.id)

    assert result == invoice_mock
    mock_session.add.assert_called_once_with(invoice_mock)
    mock_session.commit.assert_called_once()

def test_generate_invoice_subscription_not_found(mock_session):
    """
    Test that generate_invoice raises an error when the subscription
    ID does not exist in the database.
    """
    mock_session.query.return_value.get.return_value = None

    with pytest.raises(ValueError, match="Subscription not found"):
        generate_invoice(999)