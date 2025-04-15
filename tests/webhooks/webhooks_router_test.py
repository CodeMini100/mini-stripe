import pytest
from fastapi.testclient import TestClient
from main import create_app
from webhooks.webhooks_service import handle_charge_succeeded, handle_subscription_renewed


@pytest.fixture
def client():
    """
    Fixture to create and return a new FastAPI test client for each test.
    """
    app = create_app()
    return TestClient(app)


@pytest.mark.usefixtures("client")
class TestWebhookReceiverEndpoint:
    """
    Test suite for the 'webhook_receiver_endpoint' in webhooks_router.py.
    Ensures webhook signature validation and correct routing to relevant handlers.
    """

    def test_webhook_receiver_valid_charge_succeeded(self, client, mocker):
        """
        Test that a valid 'charge.succeeded' event with a correct signature
        calls the 'handle_charge_succeeded' function and returns a success status.
        """
        mock_handle_charge_succeeded = mocker.patch(
            "webhooks.webhooks_service.handle_charge_succeeded", return_value=None
        )
        event_data = {
            "type": "charge.succeeded",
            "data": {"object": {"id": "ch_123", "amount": 1000}},
        }
        headers = {"X-Webhook-Signature": "valid_signature_example"}

        response = client.post("/webhooks", json=event_data, headers=headers)

        assert response.status_code == 200, "Expected 200 OK for valid event data"
        mock_handle_charge_succeeded.assert_called_once_with(event_data)

    def test_webhook_receiver_valid_subscription_renewed(self, client, mocker):
        """
        Test that a valid 'subscription.renewed' event with a correct signature
        calls the 'handle_subscription_renewed' function and returns a success status.
        """
        mock_handle_subscription_renewed = mocker.patch(
            "webhooks.webhooks_service.handle_subscription_renewed", return_value=None
        )
        event_data = {
            "type": "subscription.renewed",
            "data": {"object": {"id": "sub_456", "plan": "premium"}},
        }
        headers = {"X-Webhook-Signature": "valid_signature_example"}

        response = client.post("/webhooks", json=event_data, headers=headers)

        assert response.status_code == 200, "Expected 200 OK for valid subscription event"
        mock_handle_subscription_renewed.assert_called_once_with(event_data)

    def test_webhook_receiver_invalid_signature(self, client, mocker):
        """
        Test that an invalid signature results in an error response, preventing
        the handler from being called.
        """
        mock_handle_charge_succeeded = mocker.patch(
            "webhooks.webhooks_service.handle_charge_succeeded"
        )
        event_data = {
            "type": "charge.succeeded",
            "data": {"object": {"id": "ch_789", "amount": 2000}},
        }
        headers = {"X-Webhook-Signature": "invalid_signature_example"}

        response = client.post("/webhooks", json=event_data, headers=headers)

        assert response.status_code == 403, "Expected 403 Forbidden for invalid signature"
        mock_handle_charge_succeeded.assert_not_called()

    def test_webhook_receiver_no_signature(self, client, mocker):
        """
        Test that no signature in headers results in an error response.
        """
        mock_handle_charge_succeeded = mocker.patch(
            "webhooks.webhooks_service.handle_charge_succeeded"
        )
        event_data = {
            "type": "charge.succeeded",
            "data": {"object": {"id": "ch_no_sig", "amount": 3000}},
        }

        # Intentionally omitting the signature header
        response = client.post("/webhooks", json=event_data)

        assert response.status_code == 400, "Expected 400 Bad Request for missing signature"
        mock_handle_charge_succeeded.assert_not_called()

    def test_webhook_receiver_unsupported_event(self, client, mocker):
        """
        Test that an unsupported event type results in an error or a specific response,
        ensuring handlers are not called.
        """
        mock_handle_charge_succeeded = mocker.patch(
            "webhooks.webhooks_service.handle_charge_succeeded"
        )
        mock_handle_subscription_renewed = mocker.patch(
            "webhooks.webhooks_service.handle_subscription_renewed"
        )
        event_data = {
            "type": "unknown.event",
            "data": {"object": {"id": "ev_unsupported"}},
        }
        headers = {"X-Webhook-Signature": "valid_signature_example"}

        response = client.post("/webhooks", json=event_data, headers=headers)

        # Depending on implementation, this might be a 400, 404, or 200 with special handling
        # Here we assume 400 for an unsupported event
        assert response.status_code == 400, "Expected 400 Bad Request for unsupported event"
        mock_handle_charge_succeeded.assert_not_called()
        mock_handle_subscription_renewed.assert_not_called()