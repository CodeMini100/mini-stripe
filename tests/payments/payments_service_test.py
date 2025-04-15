import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# Import the functions to test from the project root
from payments.payments_service import create_charge, refund_charge

@pytest.fixture
def mock_db_session():
    """
    Fixture that returns a mock Session object for testing.
    This allows us to track calls to the database without using a real DB.
    """
    return MagicMock(spec=Session)


@pytest.mark.describe("Test create_charge function")
class TestCreateCharge:
    @pytest.mark.it("Should create a charge record successfully given valid inputs")
    @patch("payments.payments_service.log_info")  # Example: mocking a logging call if it exists
    def test_create_charge_success(self, mock_log, mock_db_session):
        # Arrange
        customer_id = 123
        amount = 49.99
        payment_method = "credit_card"

        # We might want to mock an external payment call or any internal logic
        # For example, if there's a function that handles payment processing:
        with patch("payments.payments_service.simulate_payment", return_value=True) as mock_payment:
            # Act
            charge = create_charge(customer_id, amount, payment_method, db_session=mock_db_session)

            # Assert
            mock_payment.assert_called_once_with(customer_id, amount, payment_method)
            mock_db_session.add.assert_called_once()  # Check if charge was added to the session
            mock_db_session.commit.assert_called_once()  # Check if session was committed
            assert charge.customer_id == customer_id
            assert charge.amount == amount
            assert charge.payment_method == payment_method
            assert charge.status == "succeeded"  # Assuming a 'succeeded' status is set upon success

    @pytest.mark.it("Should handle error when external payment simulation fails")
    def test_create_charge_payment_failure(self, mock_db_session):
        # Arrange
        customer_id = 123
        amount = 49.99
        payment_method = "credit_card"

        # Suppose simulate_payment returns False or raises an exception on failure
        with patch("payments.payments_service.simulate_payment", return_value=False):
            # Act
            charge = create_charge(customer_id, amount, payment_method, db_session=mock_db_session)

            # Assert
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            assert charge.status == "failed"  # Assuming the service sets status to 'failed'


@pytest.mark.describe("Test refund_charge function")
class TestRefundCharge:
    @pytest.mark.it("Should successfully refund a previously succeeded charge")
    def test_refund_charge_success(self, mock_db_session):
        # Arrange
        charge_id = 999
        
        # Mock the DB to return a charge that can be refunded
        mock_charge = MagicMock()
        mock_charge.status = "succeeded"
        
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_charge

        # Act
        refunded_charge = refund_charge(charge_id, db_session=mock_db_session)

        # Assert
        assert refunded_charge.status == "refunded"
        mock_db_session.commit.assert_called_once()

    @pytest.mark.it("Should return None or handle error if charge not found")
    def test_refund_charge_not_found(self, mock_db_session):
        # Arrange
        charge_id = 404
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        # Act
        refunded_charge = refund_charge(charge_id, db_session=mock_db_session)

        # Assert
        assert refunded_charge is None  # Or check for an exception, depending on the implementation
        mock_db_session.commit.assert_not_called()

    @pytest.mark.it("Should handle already refunded charges gracefully")
    def test_refund_charge_already_refunded(self, mock_db_session):
        # Arrange
        charge_id = 888
        mock_charge = MagicMock()
        mock_charge.status = "refunded"  # Already refunded
        
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_charge

        # Act
        refunded_charge = refund_charge(charge_id, db_session=mock_db_session)

        # Assert
        assert refunded_charge.status == "refunded"  # No change
        mock_db_session.commit.assert_not_called()  # No new DB write needed if it's already refunded