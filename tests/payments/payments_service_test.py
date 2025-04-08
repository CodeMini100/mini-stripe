import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Import the functions we want to test
from ...payments.payments_service import create_charge, refund_charge
# Import any models you might need to verify database changes
# (Assuming there's a Payment model or similar in your code)
from ...models import PaymentRecord


@pytest.fixture
def db_session():
    """
    Fixture to provide a database session for tests.
    This can be configured to use an in-memory or test-specific database.
    """
    # Setup
    # Example: Use an in-memory database or a transactional context
    # session = setup_test_db_session()
    # yield session
    # Teardown
    # session.close()
    pass


class TestPaymentsService:
    """
    Tests for the payments_service module which includes create_charge and refund_charge.
    """

    @pytest.mark.parametrize(
        "customer_id, amount, payment_method",
        [
            (1, 100.00, "credit_card"),
            (2, 59.99, "paypal"),
        ],
    )
    @patch("...payments.payments_service.SomePaymentProvider")  # Example: Patch a provider
    def test_create_charge_success(
        self, mock_payment_provider, db_session, customer_id, amount, payment_method
    ):
        """
        Test that create_charge succeeds when the payment provider processes the charge without errors.
        We mock the payment provider to simulate a successful charge.
        """
        # Arrange
        mock_instance = MagicMock()
        mock_instance.charge.return_value = {"status": "success"}
        mock_payment_provider.return_value = mock_instance

        # Act
        charge_record = create_charge(customer_id, amount, payment_method)

        # Assert
        # Verify the payment provider was called
        mock_instance.charge.assert_called_once_with(
            customer_id=customer_id,
            amount=amount,
            payment_method=payment_method
        )
        # Verify that a charge record has the expected data (depending on the structure of your record)
        assert charge_record.customer_id == customer_id
        assert charge_record.amount == amount
        assert charge_record.payment_method == payment_method
        # You may also verify that the record is stored in DB if your function writes to it
        # Example: db_session.query(PaymentRecord).filter_by(id=charge_record.id).one()

    @patch("...payments.payments_service.SomePaymentProvider")  # Example: Patch a provider
    def test_create_charge_error(self, mock_payment_provider, db_session):
        """
        Test that create_charge handles an error from the payment provider gracefully.
        We mock the payment provider to raise an exception or return an error response.
        """
        # Arrange
        customer_id = 3
        amount = 200.00
        payment_method = "credit_card"

        mock_instance = MagicMock()
        mock_instance.charge.side_effect = Exception("Payment provider failed")
        mock_payment_provider.return_value = mock_instance

        # Act & Assert
        with pytest.raises(Exception, match="Payment provider failed"):
            create_charge(customer_id, amount, payment_method)

        # Verify the payment provider was called
        mock_instance.charge.assert_called_once()

    @patch("...payments.payments_service.SomePaymentProvider")  # Example: Patch a provider
    def test_refund_charge_success(self, mock_payment_provider, db_session):
        """
        Test that refund_charge updates the charge record to reflect a refund.
        We mock the payment provider to simulate a successful refund.
        """
        # Arrange
        # Create or retrieve a charge record (depending on your setup)
        # Example: assume we create a PaymentRecord object for testing
        charge_id = 10
        mock_instance = MagicMock()
        mock_instance.refund.return_value = {"status": "success"}
        mock_payment_provider.return_value = mock_instance

        # Act
        updated_record = refund_charge(charge_id)

        # Assert
        # Verify the provider was called
        mock_instance.refund.assert_called_once_with(charge_id=charge_id)
        # Check if the record was updated as expected (e.g. refunded == True)
        assert updated_record.is_refunded is True
        # You may also check DB to ensure the change was persisted
        # Example: updated_in_db = db_session.query(PaymentRecord).filter_by(id=charge_id).one()
        # assert updated_in_db.is_refunded is True

    @patch("...payments.payments_service.SomePaymentProvider")  # Example: Patch a provider
    def test_refund_charge_error(self, mock_payment_provider, db_session):
        """
        Test that refund_charge handles an error from the payment provider gracefully.
        We mock the payment provider to raise an exception.
        """
        # Arrange
        charge_id = 99
        mock_instance = MagicMock()
        mock_instance.refund.side_effect = Exception("Refund failed")
        mock_payment_provider.return_value = mock_instance

        # Act & Assert
        with pytest.raises(Exception, match="Refund failed"):
            refund_charge(charge_id)

        # Verify the provider was called
        mock_instance.refund.assert_called_once_with(charge_id=charge_id)