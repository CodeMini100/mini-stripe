import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Load application and config
from main import create_app
from config import load_config

# Import the Subscription model from subscriptions.subscriptions_models
from subscriptions.subscriptions_models import Subscription


@pytest.fixture
def sample_subscription_data():
    """
    Provides sample data for creating a test Subscription record.
    Adjust fields accordingly based on actual Subscription model columns.
    """
    return {
        "customer_id": 1,
        "plan_id": 2,
        "status": "active",
        # Add or remove fields based on the actual model definition.
    }


@pytest.fixture
def client():
    """
    Returns a FastAPI test client for integration tests.
    Assumes that create_app() sets up all routers, middleware, etc.
    """
    app = create_app()
    return TestClient(app)


def test_subscription_model_creation(test_db: Session, sample_subscription_data):
    """
    Test that a Subscription record can be successfully created and persisted to the database.
    Verifies that an auto-incremented primary key is assigned.
    """
    subscription = Subscription(**sample_subscription_data)
    test_db.add(subscription)
    test_db.commit()
    test_db.refresh(subscription)

    assert subscription.id is not None, "Subscription ID should be assigned after commit."
    assert subscription.customer_id == sample_subscription_data["customer_id"]
    assert subscription.plan_id == sample_subscription_data["plan_id"]
    assert subscription.status == sample_subscription_data["status"]


def test_subscription_model_defaults(test_db: Session):
    """
    Test that default values (if any) on the Subscription model are correctly applied.
    Example checks if 'status' defaults to 'active' if not provided.
    Adjust based on actual model defaults.
    """
    subscription = Subscription(customer_id=999, plan_id=100)
    test_db.add(subscription)
    test_db.commit()
    test_db.refresh(subscription)

    # Check default for 'status' or other fields that may have defaults
    assert subscription.status == "active", (
        "Expected default status to be 'active' if none was provided."
    )


def test_subscription_model_deletion(test_db: Session, sample_subscription_data):
    """
    Test that a Subscription record can be deleted from the database.
    Ensures referential integrity or cascade deletes are handled if configured.
    """
    subscription = Subscription(**sample_subscription_data)
    test_db.add(subscription)
    test_db.commit()
    test_db.refresh(subscription)

    # Now delete the record
    test_db.delete(subscription)
    test_db.commit()

    # Attempt to retrieve the deleted record
    deleted_record = test_db.query(Subscription).filter_by(id=subscription.id).first()
    assert deleted_record is None, "Subscription record should be removed from the database."


def test_subscription_model_validation(client: TestClient):
    """
    Example test of model-level validation if the Subscription model is used in request/response schemas.
    This test tries an endpoint call with invalid data (if applicable) and expects a 422 or similar error.
    Adjust based on actual endpoints and validation logic.
    """
    # Example endpoint: "/subscriptions/create_subscription" (put the real endpoint if it exists)
    # If there's no such endpoint, remove or adapt this test accordingly.
    invalid_payload = {
        "customer_id": None,  # Invalid because it's required
        "plan_id": "not-an-integer",  # Invalid type
    }
    response = client.post("/subscriptions/create_subscription", json=invalid_payload)

    # We expect a validation error. Adjust the status code based on how your app handles validation.
    assert response.status_code == 422, (
        "Expected a 422 Unprocessable Entity status code for invalid subscription data."
    )