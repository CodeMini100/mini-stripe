import pytest
from unittest.mock import MagicMock

# ----------------------------------------------------------------
# Import the functions to be tested from the project root modules
# ----------------------------------------------------------------
from webhooks.webhooks_service import handle_charge_succeeded, handle_subscription_renewed
# We will mock calls to payments.payments_service and subscriptions.subscriptions_service
# since those are the likely modules that handle charge/subscription logic.

# ----------------------------------------------------------------------------------------
# Test Suite for webhooks_service.py
# ----------------------------------------------------------------------------------------

@pytest.fixture
def valid_charge_event():
    """
    Returns a valid event_data dictionary commonly received from a charge succeeded webhook.
    """
    return {
        "charge_id": "ch_12345",
        "amount": 2000,
        "currency": "usd",
        "customer_id": "cus_67890",
        "status": "succeeded",
    }

@pytest.fixture
def valid_subscription_event():
    """
    Returns a valid event_data dictionary commonly received from a subscription renewal webhook.
    """
    return {
        "subscription_id": "sub_ABC123",
        "customer_id": "cus_67890",
        "plan_id": "plan_999",
        "event_type": "renewed",
    }

# ----------------------------------------------------------------------------------------
# handle_charge_succeeded(event_data) Tests
# ----------------------------------------------------------------------------------------

def test_handle_charge_succeeded_success(mocker, valid_charge_event):
    """
    Test that handle_charge_succeeded processes a valid charge event successfully and 
    routes to the payments service (mocked).
    """
    # Mocking whatever function might be called in payments_service, e.g., an update or status change.
    mock_mark_succeeded = mocker.patch("payments.payments_service.create_charge", return_value={"id": "ch_12345"})
    
    # Call the function under test
    result = handle_charge_succeeded(valid_charge_event)

    # Assert that the mock was called with expected arguments
    # (Adjust based on actual usage in your implementation)
    mock_mark_succeeded.assert_called_once_with(
        customer_id=valid_charge_event["customer_id"],
        amount=valid_charge_event["amount"],
        payment_method="webhook_succeeded_event"
    )
    
    # Assert the function returns or processes data as expected
    # (Adjust these assertions to match your implementation's return type or side effects)
    assert result is not None
    assert "id" in result

def test_handle_charge_succeeded_missing_charge_id(mocker):
    """
    Test that handle_charge_succeeded raises an error or handles the case
    where the charge_id is missing from the event_data.
    """
    bad_event_data = {
        "amount": 2000,
        "currency": "usd",
        "customer_id": "cus_67890",
        "status": "succeeded",
    }

    # We can mock the payments service to ensure it is NOT called
    mock_mark_succeeded = mocker.patch("payments.payments_service.create_charge", return_value={"id": "ch_12345"})
    
    with pytest.raises(KeyError):
        handle_charge_succeeded(bad_event_data)

    # Verify that the payment service was never called
    mock_mark_succeeded.assert_not_called()

# ----------------------------------------------------------------------------------------
# handle_subscription_renewed(event_data) Tests
# ----------------------------------------------------------------------------------------

def test_handle_subscription_renewed_success(mocker, valid_subscription_event):
    """
    Test that handle_subscription_renewed processes a valid subscription renewal event and
    calls the subscriptions service (mocked).
    """
    # Mock the service function that would be triggered upon successful renewal
    mock_generate_invoice = mocker.patch("subscriptions.subscriptions_service.generate_invoice", return_value={"invoice_id": "inv_987"})
    
    # Call the function under test
    result = handle_subscription_renewed(valid_subscription_event)

    # Assert that the mock was called with the correct subscription_id
    mock_generate_invoice.assert_called_once_with(valid_subscription_event["subscription_id"])
    
    # Assert the returned or processed data is as expected
    assert result is not None
    assert "invoice_id" in result

def test_handle_subscription_renewed_missing_subscription_id(mocker):
    """
    Test that handle_subscription_renewed raises an error or handles the scenario
    where the subscription_id is missing from the event_data.
    """
    bad_event_data = {
        "customer_id": "cus_67890",
        "plan_id": "plan_999",
        "event_type": "renewed",
    }

    mock_generate_invoice = mocker.patch("subscriptions.subscriptions_service.generate_invoice")

    with pytest.raises(KeyError):
        handle_subscription_renewed(bad_event_data)

    # Ensure no invoice generation was attempted
    mock_generate_invoice.assert_not_called()