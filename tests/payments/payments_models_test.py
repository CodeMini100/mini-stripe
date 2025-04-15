import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from pydantic import ValidationError
from datetime import datetime

# Load application and config for potential integration testing
from main import create_app
from config import load_config

# Import the models from the skeleton payments_models.py
# Payment -> PaymentSQL, PaymentCreate -> PaymentModel
from payments.payments_models import (
    Payment as PaymentSQL,
    PaymentCreate as PaymentModel,
    PaymentStatus,
)

@pytest.fixture(scope="module")
def client():
    """
    Fixture to create a TestClient instance for FastAPI app.
    If payments models require integration with the API, this client can be used.
    """
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def test_db():
    """
    Fixture for creating a temporary database session (if you have a testing database setup).
    Replace with your actual test database handling code.
    """
    # Example placeholder: In a real scenario, configure a test DB engine and session here.
    # from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker
    #
    # engine = create_engine("sqlite:///:memory:", echo=True)
    # TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base.metadata.create_all(bind=engine)
    #
    # db = TestingSessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    #
    # For now, just yield None as a placeholder.
    yield None


def test_payment_model_pydantic_valid():
    """
    Test creating a valid Pydantic payment model.
    We use PaymentCreate (aliased as PaymentModel) with fields from the skeleton:
    - amount
    - status
    """
    model_data = {
        "amount": 49.99,
        "status": "PENDING"
    }
    payment = PaymentModel(**model_data)
    assert payment.amount == 49.99
    assert payment.status == PaymentStatus.PENDING


def test_payment_model_pydantic_invalid_missing_fields():
    """
    Test creating a Pydantic payment model with missing required fields (e.g., amount).
    Expects ValidationError to be raised.
    """
    model_data = {
        # "amount": 49.99,  # Intentionally omitted
        "status": "PENDING"
    }
    with pytest.raises(ValidationError):
        PaymentModel(**model_data)


def test_payment_model_pydantic_invalid_field_type():
    """
    Test creating a Pydantic payment model with an invalid field type for 'amount'.
    Expects ValidationError to be raised.
    """
    model_data = {
        "amount": "not_a_float",  # Incorrect type
        "status": "PENDING"
    }
    with pytest.raises(ValidationError):
        PaymentModel(**model_data)


def test_payment_model_sqlalchemy_integration(test_db: Session):
    """
    Test creating and persisting a PaymentSQL (SQLAlchemy model) to the test database.
    Demonstrates a simple insert and retrieval if using real DB session.
    """
    if not test_db:
        pytest.skip("No test database session provided, skipping SQLAlchemy integration test.")

    # Use PaymentSQL with amount, status, created_at, updated_at
    new_payment = PaymentSQL(
        amount=49.99,
        status=PaymentStatus.PENDING,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Insert the record
    test_db.add(new_payment)
    test_db.commit()
    test_db.refresh(new_payment)

    # Assert the record was created
    assert new_payment.id is not None
    assert new_payment.amount == 49.99
    assert new_payment.status == PaymentStatus.PENDING


def test_payment_model_sqlalchemy_invalid_data(test_db: Session):
    """
    Test handling of invalid data for a PaymentSQL (SQLAlchemy model).
    This checks constraints or raises errors on commit if your model enforces them.
    """
    if not test_db:
        pytest.skip("No test database session provided, skipping SQLAlchemy integration test.")

    # Attempt to insert with invalid data (e.g., negative amount) if your schema forbids it
    invalid_payment = PaymentSQL(
        amount=-10,
        status=PaymentStatus.PENDING,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    test_db.add(invalid_payment)
    with pytest.raises(Exception):
        # Depending on DB constraints, this may raise an IntegrityError or similar
        test_db.commit()  # Expecting an error if negative amounts aren't allowed

    # Rollback to keep the session clean
    test_db.rollback()