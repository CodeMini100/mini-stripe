import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

def create_customer(name: str, email: str, payment_info: Dict[str, str]) -> Dict[str, str]:
    """
    Persists a new customer record in the database.

    Args:
        name (str): Name of the customer.
        email (str): Email address of the customer.
        payment_info (Dict[str, str]): Payment information for the customer.

    Returns:
        Dict[str, str]: A dictionary representing the newly created customer record.

    Raises:
        ValueError: If input parameters are invalid or data cannot be persisted.
    """
    # TODO: Implement actual database persistence logic
    try:
        if not name or not email:
            raise ValueError("Name and email are required to create a customer.")

        # NOTE: The following is a placeholder representation of a saved record
        new_customer = {
            "id": "generated_id",
            "name": name,
            "email": email,
            "payment_info": payment_info
        }

        # TODO: Replace with actual DB insert and return newly created record
        return new_customer
    except Exception as error:
        logger.error("Failed to create a new customer: %s", error)
        raise ValueError("Could not create customer record.") from error


def fetch_customer(customer_id: str) -> Optional[Dict[str, str]]:
    """
    Retrieves a customer record from the database by ID.

    Args:
        customer_id (str): The unique identifier of the customer.

    Returns:
        Optional[Dict[str, str]]: A dictionary representing the customer record if found, or None if not found.

    Raises:
        ValueError: If the customer_id parameter is invalid.
    """
    # TODO: Implement actual database lookup logic
    try:
        if not customer_id:
            raise ValueError("Customer ID is required to fetch a customer.")

        # NOTE: This is a placeholder for a found record
        # In a real scenario, if the record is not found, return None
        mock_customer = {
            "id": customer_id,
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "payment_info": {"card_number": "1234 5678 9012 3456"}
        }

        # TODO: Replace with actual DB fetch logic and return the record if found
        return mock_customer
    except Exception as error:
        logger.error("Failed to fetch the customer: %s", error)
        raise ValueError("Could not fetch customer record.") from error