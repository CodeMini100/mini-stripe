import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Import necessary modules from the project structure
from main import create_app
from config import load_config
from subscriptions.subscriptions_service import (
    create_subscription,
    cancel_subscription,
    generate_invoice
)

# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    """
    Fixture to initialize and return a TestClient for FastAPI app.
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture
def test_db():
    """
    Fixture that could provide a mocked or temporary database session.
    For unit tests, we can use a MagicMock or an in-memory DB if needed.
    """
    # Using MagicMock here as an example of a mock DB session
    return MagicMock(spec=Session)


# -------------------------------------------------------------------
# Tests for create_subscription(customer_id, plan_id)
# -------------------------------------------------------------------

@pytest.mark.parametrize(
    "customer_id, plan_id",
    [
        (1, 101),      # Example valid data
        ("abc", "xyz") # Example scenario with non-integer IDs (still valid test if types are coerced)
    ]
)
def test_create_subscription_success(test_db, customer_id, plan_id):
    """
    Test that create_subscription successfully creates a subscription record
    and sets up recurring billing when valid input is provided.
    """
    # Arrange: Mock any internal calls if needed
    # For example, if create_subscription calls a method to persist data to DB:
    # test_db.add.return_value = None
    # test_db.commit.return_value = None

    # Act
    subscription = create_subscription(customer_id, plan_id)

    # Assert
    assert subscription is not None, "Expected a valid subscription object to be returned."
    # Further asserts could check subscription fields, status, etc.


def test_create_subscription_invalid_input(test_db):
    """
    Test that create_subscription handles invalid input (e.g., missing or None customer_id/plan_id)
    by raising an exception or returning an error.
    """
    # Arrange
    invalid_customer_id = None
    invalid_plan_id = None

    # Act / Assert
    with pytest.raises(Exception):
        # Replace Exception with a more specific exception expected from your logic
        create_subscription(invalid_customer_id, invalid_plan_id)


@patch("subscriptions.subscriptions_service.log_error")
def test_create_subscription_db_error(mock_log_error, test_db):
    """
    Test scenario where an internal DB error (or any unexpected exception) occurs
    during create_subscription, ensuring it logs the error and handles it correctly.
    """
    # Arrange: Simulate DB operation throwing an exception
    test_db.add.side_effect = Exception("Database error simulation")

    # Act / Assert
    with pytest.raises(Exception):
        create_subscription(customer_id=1, plan_id=101)

    # Verify error logging was called
    mock_log_error.assert_called_once()


# -------------------------------------------------------------------
# Tests for cancel_subscription(subscription_id)
# -------------------------------------------------------------------

def test_cancel_subscription_success(test_db):
    """
    Test that cancel_subscription successfully cancels an existing subscription
    and handles proration if needed.
    """
    # Arrange: Mock or set up a subscription to be canceled
    subscription_id = 123

    # You might set up test_db to return a valid subscription record

    # Act
    result = cancel_subscription(subscription_id)

    # Assert
    assert result is True, "Expected subscription to be canceled successfully."


def test_cancel_subscription_not_found(test_db):
    """
    Test that cancel_subscription handles the case where a subscription does not exist,
    and returns or raises an appropriate error.
    """
    # Arrange
    subscription_id = 999  # Non-existent ID

    # Ensure that the DB returns None or triggers a logic that says "not found"

    # Act / Assert
    with pytest.raises(Exception):
        cancel_subscription(subscription_id)


@patch("subscriptions.subscriptions_service.log_error")
def test_cancel_subscription_db_error(mock_log_error, test_db):
    """
    Test that cancel_subscription logs and raises an exception if a DB error or
    unexpected issue occurs.
    """
    # Arrange
    subscription_id = 123
    # Simulate DB failure
    test_db.query.side_effect = Exception("Database cancel error")

    # Act / Assert
    with pytest.raises(Exception):
        cancel_subscription(subscription_id)

    # Confirm error was logged
    mock_log_error.assert_called_once()


# -------------------------------------------------------------------
# Tests for generate_invoice(subscription_id)
# -------------------------------------------------------------------

def test_generate_invoice_success(test_db):
    """
    Test that generate_invoice successfully produces an invoice for the current
    billing cycle when provided a valid subscription_id.
    """
    # Arrange
    subscription_id = 456

    # Possibly mock query result if the subscription is active

    # Act
    invoice = generate_invoice(subscription_id)

    # Assert
    assert invoice is not None, "Expected an invoice object to be returned."
    # Additional checks on invoice details can be performed here.


def test_generate_invoice_inactive_subscription(test_db):
    """
    Test generate_invoice when the subscription is not active or is canceled,
    ensuring it returns or raises an appropriate error (e.g., no invoice generated).
    """
    # Arrange
    subscription_id = 789
    # Mock a canceled subscription in the DB

    # Act / Assert
    with pytest.raises(Exception):
        generate_invoice(subscription_id)


@patch("subscriptions.subscriptions_service.log_error")
def test_generate_invoice_db_error(mock_log_error, test_db):
    """
    Test scenario in which a DB error or any unexpected exception is raised during
    invoice generation, ensuring it is handled and logged.
    """
    # Arrange
    subscription_id = 456
    test_db.query.side_effect = Exception("Database invoice error")

    # Act / Assert
    with pytest.raises(Exception):
        generate_invoice(subscription_id)

    # Verify error logging was called
    mock_log_error.assert_called_once()