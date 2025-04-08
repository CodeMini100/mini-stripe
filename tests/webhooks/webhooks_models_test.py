import pytest
from pydantic import ValidationError
from ...webhooks.webhooks_models import WebhookPayload

# ------------------------------------------------------------------------------
# Test Suite for Webhook Pydantic Models
# ------------------------------------------------------------------------------
# These tests cover validation behavior for the Pydantic models defined in
# webhooks_models.py. We test correct data, missing fields, invalid types, etc.
# ------------------------------------------------------------------------------

def test_webhook_payload_valid():
    """
    Test that providing valid data creates a valid WebhookPayload instance.
    """
    valid_data = {
        "event_name": "user_signup",
        "timestamp": "2023-10-01T12:00:00Z",
        "data": {"user_id": 123, "plan": "premium"}
    }
    payload = WebhookPayload(**valid_data)
    assert payload.event_name == "user_signup"
    assert payload.timestamp.isoformat() == "2023-10-01T12:00:00+00:00"
    assert payload.data == {"user_id": 123, "plan": "premium"}

def test_webhook_payload_missing_required_field():
    """
    Test that a required field (event_name) raises a ValidationError when missing.
    """
    invalid_data = {
        # "event_name" is intentionally missing here
        "timestamp": "2023-10-01T12:00:00Z",
        "data": {"user_id": 123}
    }
    with pytest.raises(ValidationError) as exc_info:
        WebhookPayload(**invalid_data)
    assert "event_name" in str(exc_info.value)

def test_webhook_payload_invalid_timestamp():
    """
    Test that an invalid timestamp raises a ValidationError.
    """
    invalid_data = {
        "event_name": "user_signup",
        "timestamp": "invalid_timestamp",
        "data": {"user_id": 123}
    }
    with pytest.raises(ValidationError) as exc_info:
        WebhookPayload(**invalid_data)
    assert "timestamp" in str(exc_info.value)

def test_webhook_payload_invalid_data_type():
    """
    Test that providing a non-dict to the data field raises a ValidationError.
    """
    invalid_data = {
        "event_name": "user_signup",
        "timestamp": "2023-10-01T12:00:00Z",
        "data": "this_is_not_a_dict"
    }
    with pytest.raises(ValidationError) as exc_info:
        WebhookPayload(**invalid_data)
    assert "data" in str(exc_info.value)

def test_webhook_payload_extra_fields():
    """
    Test that extra fields not defined in the model are ignored or raise an error,
    depending on the configuration in the Pydantic model.
    """
    # Adjust expectation according to model's config (e.g., extra='forbid', 'ignore', 'allow')
    # If the model forbids extra fields, ValidationError should be raised.
    # If the model ignores or allows extra fields, no error should be raised.
    data_with_extra = {
        "event_name": "user_signup",
        "timestamp": "2023-10-01T12:00:00Z",
        "data": {"user_id": 123},
        "extra_field": "unexpected_value"
    }

    # Example: If extra='forbid' in the model, we expect a ValidationError:
    # Replace the below logic with your model's configuration expectation.
    with pytest.raises(ValidationError) as exc_info:
        WebhookPayload(**data_with_extra)
    assert "extra_field" in str(exc_info.value)  # Only if extra='forbid'

# ------------------------------------------------------------------------------
# End of Test Suite
# ------------------------------------------------------------------------------