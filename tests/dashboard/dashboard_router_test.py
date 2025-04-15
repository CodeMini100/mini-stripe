import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from config import load_config
from main import create_app

# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="module")
def client():
    """
    Provides a TestClient instance for the FastAPI application.
    Loads configuration and creates the FastAPI app instance.
    """
    load_config()  # Load any necessary config
    app = create_app()  # Create the FastAPI app with all routers
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_db_session():
    """
    Provides a mock or test database session.
    In a real scenario, this might set up a temporary test database.
    For now, this is a placeholder for more complex DB mocking logic.
    """
    # Setup code or mocking could go here
    session = Session(bind=None)  # or a real test DB engine
    yield session
    # Teardown code if necessary


# -----------------------------------------------------------------------------
# Tests for get_dashboard_data_endpoint
# -----------------------------------------------------------------------------
def test_get_dashboard_data_endpoint_success(client, mock_db_session):
    """
    Tests a successful retrieval of dashboard data.
    Ensures the response returns the expected keys and a 200 status.
    """
    response = client.get("/dashboard/data")
    assert response.status_code == 200
    data = response.json()

    # Check that essential fields are present (example fields)
    assert "recent_charges" in data
    assert "new_customers" in data
    assert "subscription_metrics" in data


def test_get_dashboard_data_endpoint_no_records(client, mock_db_session, monkeypatch):
    """
    Tests the endpoint when there are no records in the database.
    Mocks or simulates an empty database result to ensure the endpoint
    handles it gracefully.
    """

    # Example of mocking if needed:
    # def mock_empty_data(*args, **kwargs):
    #     return []
    # monkeypatch.setattr("some_module.some_method", mock_empty_data)

    response = client.get("/dashboard/data")
    assert response.status_code == 200
    data = response.json()

    # Expecting empty or default values for metrics
    assert data.get("recent_charges") == []
    assert data.get("new_customers") == []
    assert data.get("subscription_metrics") == {}


def test_get_dashboard_data_endpoint_server_error(client, monkeypatch):
    """
    Simulates a server error case by monkeypatching
    the underlying function to raise an exception.
    Verifies the endpoint returns a 500 status code.
    """

    def mock_raise_exception():
        raise Exception("Simulated server error")

    # Example patch: we'd replace the actual business logic call with a failing version
    monkeypatch.setattr("dashboard.dashboard_router.get_dashboard_data_endpoint", mock_raise_exception)

    response = client.get("/dashboard/data")
    assert response.status_code == 500


# -----------------------------------------------------------------------------
# Tests for get_transaction_details_endpoint
# -----------------------------------------------------------------------------
def test_get_transaction_details_endpoint_success(client, mock_db_session):
    """
    Tests a successful retrieval of a specific transaction's details.
    Ensures the response returns the expected charge data and status code.
    """
    test_charge_id = "ch_12345"  # Example test charge ID
    response = client.get(f"/dashboard/transactions/{test_charge_id}")
    assert response.status_code == 200
    data = response.json()

    # Check that essential fields are present (example fields)
    assert data.get("charge_id") == test_charge_id
    assert "amount" in data
    assert "status" in data


def test_get_transaction_details_endpoint_not_found(client, mock_db_session):
    """
    Tests the endpoint when the specified charge ID does not exist in the database.
    Verifies that a 404 Not Found response is returned.
    """
    non_existent_charge_id = "ch_00000"
    response = client.get(f"/dashboard/transactions/{non_existent_charge_id}")
    assert response.status_code == 404
    assert response.json().get("detail") == "Charge not found"


def test_get_transaction_details_endpoint_server_error(client, monkeypatch):
    """
    Simulates a server error when attempting to retrieve charge details.
    Verifies the endpoint returns a 500 status code.
    """

    def mock_raise_exception(charge_id: str):
        raise Exception("Simulated server error")

    monkeypatch.setattr("dashboard.dashboard_router.get_transaction_details_endpoint", mock_raise_exception)

    response = client.get("/dashboard/transactions/ch_any")
    assert response.status_code == 500