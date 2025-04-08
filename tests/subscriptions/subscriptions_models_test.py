import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from ...models import Base  # Adjust if your project's Base or metadata is located elsewhere
from ...subscriptions.subscriptions_models import Subscription  # Adjust the import to match actual model names

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture(scope="module")
def test_engine():
    """
    Creates an in-memory SQLite engine for testing.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_engine) -> Session:
    """
    Provides a session to interact with the test database.
    Ensures tests run in isolation with rollback after each test.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------

def test_subscription_model_create_success(db_session: Session):
    """
    Test creating a Subscription model successfully with valid data.
    """
    new_subscription = Subscription(
        name="Test Plan",
        price=9.99
        # Include other required fields or defaults as defined in your model
    )
    db_session.add(new_subscription)
    db_session.commit()
    db_session.refresh(new_subscription)

    assert new_subscription.id is not None, "Subscription ID should be auto-generated"
    assert new_subscription.name == "Test Plan", "Subscription name mismatch"
    assert new_subscription.price == 9.99, "Subscription price mismatch"
    # If there's an is_active default
    if hasattr(new_subscription, "is_active"):
        assert new_subscription.is_active is True, "Subscription should be active by default"


def test_subscription_model_create_failure(db_session: Session):
    """
    Test that creating a Subscription with missing or invalid required fields
    raises an IntegrityError or appropriate validation error.
    """
    # Example: Missing 'name' if your model enforces non-null on 'name'
    invalid_subscription = Subscription(
        # name is missing here
        price=5.00
    )
    db_session.add(invalid_subscription)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_subscription_model_update(db_session: Session):
    """
    Test updating a Subscription record in the database.
    """
    # First, create a valid subscription
    subscription = Subscription(name="Update Plan", price=10.0)
    db_session.add(subscription)
    db_session.commit()
    db_session.refresh(subscription)

    # Now update the subscription
    subscription.name = "Updated Plan Name"
    subscription.price = 12.50
    db_session.commit()
    db_session.refresh(subscription)

    assert subscription.name == "Updated Plan Name", "Subscription name should be updated"
    assert subscription.price == 12.50, "Subscription price should be updated"


def test_subscription_model_delete(db_session: Session):
    """
    Test deleting a Subscription record from the database.
    """
    subscription = Subscription(name="Delete Plan", price=7.99)
    db_session.add(subscription)
    db_session.commit()
    db_session.refresh(subscription)

    sub_id = subscription.id
    db_session.delete(subscription)
    db_session.commit()

    deleted = db_session.query(Subscription).filter_by(id=sub_id).first()
    assert deleted is None, "Subscription record should be deleted"


@pytest.mark.parametrize("price_value", [-1, None, 0, 100])
def test_subscription_model_price_values(db_session: Session, price_value):
    """
    Test various valid and invalid price values for Subscription.
    Modify the assertions based on your validation rules (e.g. price >= 0).
    """
    subscription = Subscription(name="Parametrized Plan", price=price_value)
    db_session.add(subscription)
    if price_value is None or price_value < 0:
        with pytest.raises(IntegrityError):
            db_session.commit()
    else:
        db_session.commit()
        db_session.refresh(subscription)
        assert subscription.price == price_value, "Subscription price did not match expected value"