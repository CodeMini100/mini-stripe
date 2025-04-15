import pytest
from pydantic import ValidationError

# NOTE: The following import assumes that the "customers_models.py" file
# contains one or more Pydantic models to represent a Customer. Adjust
# the import and model names according to your actual implementation.
from customers.customers_models import Customer  # Example: If the model is named "Customer"


@pytest.mark.describe("Customers Models - Pydantic Validation")
class TestCustomerPydanticModel:
    """
    Test suite for Pydantic customer models in customers.customers_models.py.
    These tests ensure that the model enforces correct field constraints
    and validation for valid and invalid data.
    """

    @pytest.mark.it("Should successfully create a Customer model with valid data")
    def test_create_customer_model_valid_data(self):
        """
        Test that instantiating the Customer model with valid data
        does not raise an error and sets fields correctly.
        """
        valid_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "payment_info": "tok_visa_1234",
        }

        customer = Customer(**valid_data)
        assert customer.name == valid_data["name"]
        assert customer.email == valid_data["email"]
        assert customer.payment_info == valid_data["payment_info"]

    @pytest.mark.it("Should raise ValidationError when required fields are missing")
    def test_create_customer_model_missing_required_fields(self):
        """
        Test that missing required fields (e.g., 'name', 'email') raises ValidationError.
        Adjust the test data to match your model's required fields.
        """
        invalid_data = {
            # 'name' is missing
            "email": "john.doe@example.com",
            "payment_info": "tok_visa_1234",
        }

        with pytest.raises(ValidationError):
            Customer(**invalid_data)

    @pytest.mark.it("Should raise ValidationError for invalid email format")
    def test_create_customer_model_invalid_email(self):
        """
        Test that providing an invalid email raises ValidationError.
        """
        invalid_data = {
            "name": "John Doe",
            "email": "not-an-email",
            "payment_info": "tok_visa_1234",
        }

        with pytest.raises(ValidationError):
            Customer(**invalid_data)