import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Import the functions to test from the service
from customers.customers_service import create_customer, fetch_customer


@pytest.fixture
def mock_session():
    """
    Fixture that provides a mock SQLAlchemy session.
    This can be used to simulate database operations.
    """
    return MagicMock(spec=Session)


@pytest.mark.describe("create_customer() function tests")
class TestCreateCustomer:

    @pytest.mark.it("Successfully creates a customer with valid data")
    def test_create_customer_success(self, mock_session):
        """
        Test that create_customer() calls the necessary DB operations
        and returns the correct customer data when provided valid inputs.
        """
        # Arrange
        name = "John Doe"
        email = "john.doe@example.com"
        payment_info = {"card_number": "4242424242424242"}

        # Mocking the returned customer object
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.email = email

        # Mock the session's add and commit behavior
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        # We might assume the function returns the newly created customer
        with patch("customers.customers_service.Customer", return_value=mock_customer):
            # Act
            created_customer = create_customer(name, email, payment_info)

        # Assert
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        assert created_customer.name == name
        assert created_customer.email == email

    @pytest.mark.it("Fails to create a customer with invalid email")
    def test_create_customer_failure_invalid_email(self, mock_session):
        """
        Test that create_customer() raises an exception or returns None/False
        when provided an invalid email format.
        """
        # Arrange
        name = "John Doe"
        invalid_email = "invalid-email"
        payment_info = {"card_number": "4242424242424242"}

        # Depending on implementation, it might throw an exception.
        # We'll assume a ValueError for an invalid email.
        with pytest.raises(ValueError) as exc_info:
            create_customer(name, invalid_email, payment_info)

        # Assert the exception message (optional)
        assert "Invalid email" in str(exc_info.value)


@pytest.mark.describe("fetch_customer() function tests")
class TestFetchCustomer:

    @pytest.mark.it("Successfully fetches an existing customer by ID")
    def test_fetch_customer_success(self, mock_session):
        """
        Test that fetch_customer() returns a valid customer
        when provided a customer_id that exists in the DB.
        """
        # Arrange
        customer_id = 123
        mock_customer = MagicMock()
        mock_customer.id = customer_id
        mock_customer.name = "Jane Doe"
        mock_customer.email = "jane.doe@example.com"

        # Simulate the session's query filter returning our mock customer
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_customer

        # Act
        with patch("customers.customers_service.Session", return_value=mock_session):
            fetched = fetch_customer(customer_id)

        # Assert
        assert fetched is not None
        assert fetched.id == customer_id
        assert fetched.name == "Jane Doe"
        assert fetched.email == "jane.doe@example.com"

    @pytest.mark.it("Returns None if the customer does not exist")
    def test_fetch_customer_not_found(self, mock_session):
        """
        Test that fetch_customer() returns None when no matching customer
        is found in the database.
        """
        # Arrange
        non_existent_id = 999
        mock_session.query.return_value.filter_by.return_value.first.return_value = None

        # Act
        with patch("customers.customers_service.Session", return_value=mock_session):
            fetched = fetch_customer(non_existent_id)

        # Assert
        assert fetched is None