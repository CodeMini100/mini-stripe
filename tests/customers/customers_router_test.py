import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Required model import (adapt as needed for your actual model):
from ...models import YourModel

# Import the router or endpoints from the customers_router file
from ...customers.customers_router import router


@pytest.fixture(scope="module")
def test_app():
    """
    Create a FastAPI test application by including the customers router.
    This fixture is used to generate a TestClient for HTTP requests.
    """
    app = FastAPI()
    app.include_router(router, prefix="/customers", tags=["customers"])
    yield app


@pytest.fixture(scope="module")
def client(test_app):
    """
    Returns a TestClient instance for sending requests to the FastAPI test application.
    """
    return TestClient(test_app)


@pytest.fixture
def db_session():
    """
    Provide a mock or real database session for testing database operations.
    This fixture should be adjusted to reflect your test database setup.
    """
    # Set up your test database session here
    session = Session()  # This is symbolic; replace with your actual session setup.
    yield session
    # Teardown logic (close connection, rollback, etc.) goes here


def test_create_customer_success(client, db_session):
    """
    Test creating a new customer with valid data.
    Expects a successful response and a newly created customer record.
    """
    valid_payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com"
    }

    response = client.post("/customers", json=valid_payload)
    assert response.status_code == 201, "Expected customer creation to return a 201 status code"
    data = response.json()
    assert "id" in data, "Response JSON should contain 'id' after successful creation"
    assert data["name"] == valid_payload["name"], "Customer name in response should match input"
    assert data["email"] == valid_payload["email"], "Customer email in response should match input"


def test_create_customer_missing_fields(client, db_session):
    """
    Test creating a new customer with missing required fields.
    Expects a validation or bad request error response.
    """
    invalid_payload = {
        "name": "John Doe"
        # 'email' is missing
    }

    response = client.post("/customers", json=invalid_payload)
    assert response.status_code in [400, 422], "Expected a 400 or 422 status code for missing fields"


def test_get_customer_success(client, db_session):
    """
    Test fetching an existing customer's details by ID.
    Expects a successful response with the correct customer data.
    """
    # First, create a customer to have a valid ID to retrieve.
    create_response = client.post("/customers", json={"name": "Bob Smith", "email": "bob.smith@example.com"})
    assert create_response.status_code == 201, "Expected customer creation to succeed for test setup"
    created_customer = create_response.json()
    created_id = created_customer["id"]

    # Now, retrieve the newly created customer
    get_response = client.get(f"/customers/{created_id}")
    assert get_response.status_code == 200, "Expected to successfully retrieve a customer by valid ID"
    fetched_customer = get_response.json()
    assert fetched_customer["id"] == created_id, "Fetched customer ID should match the created ID"
    assert fetched_customer["name"] == "Bob Smith", "Fetched customer name should match the created customer"
    assert fetched_customer["email"] == "bob.smith@example.com", "Fetched customer email should match the created customer"


def test_get_customer_not_found(client, db_session):
    """
    Test requesting a customer with an ID that does not exist.
    Expects a 404 status code for non-existent resource.
    """
    non_existent_id = 999999999
    response = client.get(f"/customers/{non_existent_id}")
    assert response.status_code == 404, "Expected 404 when retrieving a non-existent customer"
