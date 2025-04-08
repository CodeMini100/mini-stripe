import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# Import the functions to be tested from the customers_service module
from ...customers.customers_service import create_customer, fetch_customer

# Import your models if needed
# from ...models import Customer


@pytest.fixture
def mock_db_session():
    """
    Pytest fixture to create and return a mock Session object.
    This fixture can be used to simulate interactions with the database
    without requiring a real connection.
    """
    return MagicMock(spec=Session)


@pytest.mark.describe("Test create_customer function")
class TestCreateCustomer:
    @pytest.mark.it("Successfully creates a new customer record")
    def test_create_customer_success(self, mock_db_session):
        """
        Test that create_customer correctly adds a new customer record to the database
        and commits the transaction.
        """
        # Arrange: Define sample input data
        name = "John Doe"
        email = "john@example.com"
        payment_info = {"card_number": "1234-5678-9012-3456"}
        
        # Act: Call the function under test
        new_customer = create_customer(name, email, payment_info, db=mock_db_session)
        
        # Assert: Verify that the session was used to add and commit the new record
        assert mock_db_session.add.called, "Expected session.add to be called"
        assert mock_db_session.commit.called, "Expected session.commit to be called"
        assert new_customer.name == name, "Expected returned customer's name to match"
        assert new_customer.email == email, "Expected returned customer's email to match"
        assert new_customer.payment_info == payment_info, "Expected returned payment info to match"

    @pytest.mark.it("Raises an exception when the database commit fails")
    def test_create_customer_db_error(self, mock_db_session):
        """
        Test that create_customer raises an exception when the session.commit call fails.
        """
        # Arrange: Configure the mock to raise an exception on commit
        mock_db_session.commit.side_effect = Exception("Database error")
        
        # Act & Assert: The function should raise an exception, indicating a failed commit
        with pytest.raises(Exception) as exc_info:
            create_customer("Fail", "fail@example.com", {"card_number": "0000"}, db=mock_db_session)
        
        assert "Database error" in str(exc_info.value), "Expected a 'Database error' exception message"


@pytest.mark.describe("Test fetch_customer function")
class TestFetchCustomer:
    @pytest.mark.it("Successfully fetches an existing customer by ID")
    def test_fetch_customer_success(self, mock_db_session):
        """
        Test that fetch_customer returns the correct customer object
        when a valid customer_id is provided.
        """
        # Arrange: Create a mock customer object to be returned by the session
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = "Jane Doe"
        mock_customer.email = "jane@example.com"
        mock_db_session.query().filter_by().first.return_value = mock_customer
        
        # Act: Call the function under test
        found_customer = fetch_customer(mock_customer.id, db=mock_db_session)
        
        # Assert: Verify the correct customer object is returned
        assert found_customer == mock_customer, "Expected to fetch the mock customer object"
        assert found_customer.id == 1, "Expected customer ID to match"

    @pytest.mark.it("Returns None when the customer does not exist in the database")
    def test_fetch_customer_not_found(self, mock_db_session):
        """
        Test that fetch_customer returns None when the specified customer_id does not exist.
        """
        # Arrange: Configure the mock to return None
        mock_db_session.query().filter_by().first.return_value = None
        
        # Act: Call the function with a non-existent customer ID
        result = fetch_customer(999, db=mock_db_session)
        
        # Assert: Verify that None is returned when the customer is not found
        assert result is None, "Expected no customer to be returned"