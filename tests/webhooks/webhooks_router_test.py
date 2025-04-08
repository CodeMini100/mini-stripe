import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Import the router or the specific endpoint function you want to test
from ...webhooks.webhooks_router import router


@pytest.fixture(scope="module")
def test_app():
    """
    Create a FastAPI test application that includes the webhook router.
    """
    app = FastAPI()
    app.include_router(router, prefix="/webhooks")
    return app


@pytest.fixture(scope="module")
def client(test_app):
    """
    Provide a TestClient instance for making requests to the FastAPI test application.
    """
    return TestClient(test_app)


@pytest.mark.describe("webhook_receiver_endpoint - Success Cases")
class TestWebhookReceiverSuccess:
    @pytest.mark.it("Should return 200 when the signature is valid and event is handled successfully")
    @patch("...webhooks.webhooks_router.validate_signature")
    @patch("...webhooks.webhooks_router.route_event_to_handler")
    def test_valid_signature_and_event_handled(
        self,
        mock_route_event_to_handler,
        mock_validate_signature,
        client
    ):
        """
        Test that the endpoint correctly processes a webhook when
        the signature is valid and the event is routed successfully.
        """
        # Mock the signature validation to return True
        mock_validate_signature.return_value = True
        # Mock the event handler to simulate successful handling
        mock_route_event_to_handler.return_value = {"status": "success"}

        # Example request data and headers
        request_data = {"event_type": "test_event", "payload": "some_data"}
        headers = {"X-Signature": "valid_signature"}

        response = client.post(
            "/webhooks/webhook_receiver_endpoint",
            json=request_data,
            headers=headers
        )

        assert response.status_code == 200
        assert response.json() == {"status": "success"}
        mock_validate_signature.assert_called_once_with(request_data, headers)
        mock_route_event_to_handler.assert_called_once_with(request_data)

    @pytest.mark.it("Should call the correct handler based on event_type")
    @patch("...webhooks.webhooks_router.validate_signature")
    @patch("...webhooks.webhooks_router.route_event_to_handler")
    def test_correct_handler_called_based_on_event_type(
        self,
        mock_route_event_to_handler,
        mock_validate_signature,
        client
    ):
        """
        Test that the endpoint calls the correct event handler based on the event_type.
        """
        mock_validate_signature.return_value = True
        mock_route_event_to_handler.return_value = {"status": "handler_called"}

        request_data = {"event_type": "another_event", "payload": "some_data"}
        headers = {"X-Signature": "valid_signature"}

        response = client.post(
            "/webhooks/webhook_receiver_endpoint",
            json=request_data,
            headers=headers
        )

        assert response.status_code == 200
        assert response.json() == {"status": "handler_called"}
        mock_validate_signature.assert_called_once()
        mock_route_event_to_handler.assert_called_once_with(request_data)


@pytest.mark.describe("webhook_receiver_endpoint - Error Cases")
class TestWebhookReceiverErrors:
    @pytest.mark.it("Should return 400 when X-Signature header is missing")
    def test_missing_signature_header(self, client):
        """
        Test that the endpoint rejects requests without the X-Signature header with a 400 error.
        """
        request_data = {"event_type": "test_event", "payload": "some_data"}
        headers = {}  # No signature

        response = client.post(
            "/webhooks/webhook_receiver_endpoint",
            json=request_data,
            headers=headers
        )

        assert response.status_code == 400
        assert "Missing signature header" in response.text

    @pytest.mark.it("Should return 401 when signature is invalid")
    @patch("...webhooks.webhooks_router.validate_signature")
    def test_invalid_signature(self, mock_validate_signature, client):
        """
        Test that the endpoint rejects requests with an invalid signature with a 401 error.
        """
        mock_validate_signature.return_value = False

        request_data = {"event_type": "test_event", "payload": "some_data"}
        headers = {"X-Signature": "invalid_signature"}

        response = client.post(
            "/webhooks/webhook_receiver_endpoint",
            json=request_data,
            headers=headers
        )

        assert response.status_code == 401
        assert "Invalid signature" in response.text

    @pytest.mark.it("Should return 400 when event_type is missing in the request data")
    @patch("...webhooks.webhooks_router.validate_signature")
    def test_missing_event_type(self, mock_validate_signature, client):
        """
        Test that the endpoint returns 400 if the event_type field is missing from the request body.
        """
        # Mock the signature validation to return True
        mock_validate_signature.return_value = True

        request_data = {"payload": "some_data"}  # No event_type
        headers = {"X-Signature": "valid_signature"}

        response = client.post(
            "/webhooks/webhook_receiver_endpoint",
            json=request_data,
            headers=headers
        )

        assert response.status_code == 400
        assert "Missing event_type" in response.text

    @pytest.mark.it("Should return 500 when an unexpected exception occurs in the handler")
    @patch("...webhooks.webhooks_router.validate_signature")
    @patch("...webhooks.webhooks_router.route_event_to_handler")
    def test_unexpected_exception_in_handler(
        self,
        mock_route_event_to_handler,
        mock_validate_signature,
        client
    ):
        """
        Test that the endpoint returns 500 when an unhandled exception occurs 
        during event routing or handler execution.
        """
        mock_validate_signature.return_value = True
        # Force an exception to be raised in the event handler
        mock_route_event_to_handler.side_effect = Exception("Unexpected Error")

        request_data = {"event_type": "test_event", "payload": "some_data"}
        headers = {"X-Signature": "valid_signature"}

        response = client.post(
            "/webhooks/webhook_receiver_endpoint",
            json=request_data,
            headers=headers
        )

        assert response.status_code == 500
        assert "Unexpected Error" in response.text
