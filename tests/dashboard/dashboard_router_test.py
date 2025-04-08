import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock

# Import your router and any necessary models from the main project
from ...dashboard.dashboard_router import router
from ...models import YourModel  # Replace with actual model(s) used in the dashboard router

@pytest.fixture
def test_app():
    """
    Fixture to create a FastAPI test application including the dashboard router.
    """
    app = FastAPI()
    app.include_router(router, prefix="/dashboard", tags=["dashboard"])
    return app

@pytest.fixture
def client(test_app):
    """
    Fixture to provide a TestClient for sending requests to the test application.
    """
    return TestClient(test_app)

@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mock database session object for testing.
    """
    # You can customize this mock to fit your actual DB queries.
    mock_session = MagicMock(spec=Session)
    return mock_session

@pytest.mark.describe("Dashboard Data Endpoint Tests")
class TestGetDashboardDataEndpoint:
    @pytest.mark.it("should return 200 and summarize recent charges, new customers, and subscription metrics when data is available")
    @patch("...dashboard.dashboard_router.some_database_call")  # Example mock path, replace with actual call
    def test_get_dashboard_data_success(self, mock_db_call, client, mock_db_session):
        """
        Test that the endpoint returns valid summary data (recent charges, etc.) and status code 200.
        """
        # Arrange: mock the database call to return sample data
        mock_db_call.return_value = {
            "recent_charges": [{"id": 1, "amount": 1000}],
            "new_customers": 5,
            "subscription_metrics": {"active_subscriptions": 10, "canceled_subscriptions": 2}
        }

        # Act: send GET request to the dashboard data endpoint
        response = client.get("/dashboard/data")

        # Assert: check that the response is correct
        assert response.status_code == 200
        assert response.json() == {
            "recent_charges": [{"id": 1, "amount": 1000}],
            "new_customers": 5,
            "subscription_metrics": {"active_subscriptions": 10, "canceled_subscriptions": 2}
        }

    @pytest.mark.it("should handle database errors gracefully and return an error response with 500 status code")
    @patch("...dashboard.dashboard_router.some_database_call")  # Example mock path, replace
    def test_get_dashboard_data_db_error(self, mock_db_call, client, mock_db_session):
        """
        Test that the endpoint returns a 500 error if there's a database error while fetching data.
        """
        # Arrange: simulate a database exception
        mock_db_call.side_effect = Exception("Database failure")

        # Act
        response = client.get("/dashboard/data")

        # Assert
        assert response.status_code == 500
        assert "error" in response.json()
        assert response.json()["error"] == "Database failure"


@pytest.mark.describe("Transaction Details Endpoint Tests")
class TestGetTransactionDetailsEndpoint:
    @pytest.mark.it("should return transaction details for a valid charge_id with status code 200")
    @patch("...dashboard.dashboard_router.get_charge_by_id")  # Example mock path, replace with actual name
    def test_get_transaction_details_success(self, mock_db_call, client, mock_db_session):
        """
        Test that a valid transaction detail is returned when a correct charge_id is provided.
        """
        # Arrange
        test_charge_id = "charge_12345"
        mock_db_call.return_value = {
            "id": test_charge_id,
            "amount": 2000,
            "currency": "USD",
            "customer_id": "cust_6789"
        }

        # Act
        response = client.get(f"/dashboard/transactions/{test_charge_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_charge_id
        assert data["amount"] == 2000
        assert data["currency"] == "USD"
        assert data["customer_id"] == "cust_6789"

    @pytest.mark.it("should return 404 if the transaction with the given charge_id does not exist")
    @patch("...dashboard.dashboard_router.get_charge_by_id")  # Example mock path, replace
    def test_get_transaction_details_not_found(self, mock_db_call, client, mock_db_session):
        """
        Test that a 404 is returned when the charge_id doesn't match any transaction in the database.
        """
        # Arrange
        test_charge_id = "non_existent_charge"
        mock_db_call.return_value = None  # No transaction found

        # Act
        response = client.get(f"/dashboard/transactions/{test_charge_id}")

        # Assert
        assert response.status_code == 404
        assert "detail" in response.json()
        assert response.json()["detail"] == "Charge not found."

    @pytest.mark.it("should handle invalid charge_id format and return a 422 validation error")
    def test_get_transaction_details_invalid_charge_id(self, client):
        """
        Test that a 422 is returned when the charge_id is invalid or malformed.
        """
        # For example, passing an int where a string is expected might cause validation issues.
        invalid_charge_id = 123  # Suppose the endpoint strictly expects a string
        response = client.get(f"/dashboard/transactions/{invalid_charge_id}")

        # Assert
        assert response.status_code == 422
        # The exact structure of the error can vary, just check it's a validation error
        assert "detail" in response.json() and "type" in str(response.json()["detail"])