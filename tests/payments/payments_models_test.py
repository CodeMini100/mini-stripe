import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Adjust these imports based on actual models/classes in payments_models.py
from ...payments.payments_models import PaymentBase, PaymentCreate, PaymentUpdate, PaymentInDB
# If you have SQLAlchemy models instead of Pydantic, import them accordingly:
# from ...payments.payments_models import Payment

###############################################################################
# Fixtures
###############################################################################

@pytest.fixture
def valid_payment_data():
    """
    Returns a dictionary with valid payment data for Pydantic model testing.
    """
    return {
        "amount": 99.99,
        "currency": "USD",
        "status": "completed",
        "description": "Test payment"
    }

@pytest.fixture
def invalid_payment_data():
    """
    Returns a dictionary with invalid payment data (e.g., negative amount).
    """
    return {
        "amount": -10.00,  # Invalid negative amount
        "currency": "USD",
        "status": "pending",
        "description": "Invalid payment"
    }

@pytest.fixture
def db_test_session():
    """
    Example fixture for providing a test database session.
    Adjust this to match your actual database setup and teardown.
    """
    # from ...database import SessionLocalForTests  # Example if you have a dedicated test DB session
    # session = SessionLocalForTests()
    # yield session
    # session.close()
    # For demonstration, we'll just return None.
    return None

###############################################################################
# Pydantic Model Tests
###############################################################################

def test_create_payment_base_with_valid_data(valid_payment_data):
    """
    Test creating a PaymentBase model with valid data.
    Expect successful instantiation and matching field values.
    """
    model_instance = PaymentBase(**valid_payment_data)
    assert model_instance.amount == 99.99
    assert model_instance.currency == "USD"
    assert model_instance.status == "completed"
    assert model_instance.description == "Test payment"


def test_create_payment_base_with_invalid_data_raises_value_error(invalid_payment_data):
    """
    Test creating a PaymentBase model with invalid data.
    Expect a validation error (ValueError) due to negative amount or other constraints.
    """
    with pytest.raises(ValueError):
        PaymentBase(**invalid_payment_data)


def test_create_payment_create_model(valid_payment_data):
    """
    Test creating a PaymentCreate model with valid data.
    Can include additional logic specific to the creation process.
    """
    create_model = PaymentCreate(**valid_payment_data)
    assert create_model.amount == 99.99
    assert create_model.currency == "USD"
    assert create_model.status == "completed"


def test_update_payment_model():
    """
    Test the PaymentUpdate model to ensure partial updates work as expected.
    """
    update_data = {
        "amount": 150.00,
        "status": "refunded"
    }
    update_model = PaymentUpdate(**update_data)
    assert update_model.amount == 150.00
    assert update_model.status == "refunded"
    assert update_model.currency is None  # Not provided, should remain None


def test_payment_in_db_model(valid_payment_data):
    """
    Test PaymentInDB model which may hold additional fields
    like database ID, timestamps, etc.
    """
    in_db_data = {**valid_payment_data, "id": 1}
    in_db_model = PaymentInDB(**in_db_data)
    assert in_db_model.id == 1
    assert in_db_model.amount == 99.99
    assert in_db_model.status == "completed"

###############################################################################
# SQLAlchemy Model Tests (If applicable)
# Uncomment and adjust if you are using SQLAlchemy models in payments_models.py
###############################################################################
"""
def test_create_payment_record_in_db(db_test_session: Session, valid_payment_data):
    '''
    Test creating and storing a payment record in the database using SQLAlchemy.
    Replace Payment below with your actual SQLAlchemy model class if applicable.
    '''
    new_payment = Payment(**valid_payment_data)
    db_test_session.add(new_payment)
    db_test_session.commit()
    db_test_session.refresh(new_payment)

    # Verify the new record was saved and has an ID
    assert new_payment.id is not None
    assert new_payment.amount == valid_payment_data["amount"]
    assert new_payment.currency == valid_payment_data["currency"]


def test_query_payment_record_from_db(db_test_session: Session, valid_payment_data):
    '''
    Test querying a payment record from the database using SQLAlchemy.
    Replace Payment below with your actual SQLAlchemy model class if applicable.
    '''
    new_payment = Payment(**valid_payment_data)
    db_test_session.add(new_payment)
    db_test_session.commit()
    db_test_session.refresh(new_payment)

    # Query the payment by its primary key
    fetched_payment = db_test_session.query(Payment).get(new_payment.id)
    assert fetched_payment is not None
    assert fetched_payment.amount == valid_payment_data["amount"]
    assert fetched_payment.currency == valid_payment_data["currency"]
"""
