import pytest
from pydantic import ValidationError
# Change the import to pull in WebhookEvent and rename it to WebhookEventModel
from webhooks.webhooks_models import WebhookEvent as WebhookEventModel

@pytest.mark.describe("WebhookEventModel Validation Tests")
class TestWebhookEventModel:
    """
    Tests for Pydantic model(s) within webhooks.webhooks_models.py
    that validate incoming webhook event payloads.

    Update model fields and test data to match actual definitions
    in the webhooks.webhooks_models module.
    """

    @pytest.mark.it("Should successfully create a valid WebhookEventModel instance")
    def test_webhook_event_model_valid(self):
        valid_data = {
            "event_type": "charge.succeeded",
            "data": {"charge_id": "ch_123", "amount": 1000},
            "signature": "abc123"
        }
        event_instance = WebhookEventModel(**valid_data)
        assert event_instance.event_type == valid_data["event_type"]
        assert event_instance.data == valid_data["data"]
        assert event_instance.signature == valid_data["signature"]

    @pytest.mark.it("Should raise ValidationError if required fields are missing")
    def test_webhook_event_model_missing_fields(self):
        invalid_data = {
            # "event_type" is missing
            "data": {"charge_id": "ch_123", "amount": 1000},
            "signature": "abc123"
        }
        with pytest.raises(ValidationError):
            WebhookEventModel(**invalid_data)

    @pytest.mark.it("Should raise ValidationError for invalid field types")
    def test_webhook_event_model_invalid_types(self):
        invalid_data = {
            "event_type": 1234,  # Should be a string
            "data": "should_be_a_dict",
            "signature": 5678
        }
        with pytest.raises(ValidationError):
            WebhookEventModel(**invalid_data)