import logging
import uuid
from typing import Dict, Any

# In-memory store for demonstration purposes
# TODO: Replace with a real database or persistent storage in production
charges_db: Dict[str, Dict[str, Any]] = {}

logger = logging.getLogger(__name__)


class PaymentServiceError(Exception):
    """
    Custom exception class for payment service-related errors.
    """
    pass


def create_charge(customer_id: str, amount: float, payment_method: str) -> Dict[str, Any]:
    """
    Creates a new charge for a given customer, storing charge details
    and simulating or calling a real payment provider for processing.

    :param customer_id: The ID of the customer to be charged.
    :param amount: The amount to be charged.
    :param payment_method: The payment method used for the charge.
    :return: A dictionary representing the created charge.
    :raises PaymentServiceError: If creating or processing the charge fails.
    """
    # Generate a unique charge ID
    charge_id = str(uuid.uuid4())

    # Prepare charge details
    charge_details = {
        "charge_id": charge_id,
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": "pending",
    }

    try:
        # Simulate storing the charge record
        charges_db[charge_id] = charge_details

        # TODO: Integrate with a real payment provider instead of simulation
        logger.debug("Simulating payment process for charge_id=%s", charge_id)
        # Simulate success
        charge_details["status"] = "successful"

        logger.info("Charge created successfully: %s", charge_details)
        return charge_details
    except Exception as e:
        logger.error("Error creating charge: %s", e)
        raise PaymentServiceError("Failed to create charge") from e


def refund_charge(charge_id: str) -> Dict[str, Any]:
    """
    Issues a refund for an existing charge by updating the record
    to reflect a refunded status.

    :param charge_id: The ID of the charge to be refunded.
    :return: A dictionary representing the updated charge.
    :raises PaymentServiceError: If the charge cannot be found or refund fails.
    """
    try:
        # Retrieve existing charge
        charge_details = charges_db.get(charge_id)
        if not charge_details:
            raise PaymentServiceError("Charge not found")

        # Update charge status to refunded
        # TODO: Integrate with a real payment provider for refund
        charge_details["status"] = "refunded"

        logger.info("Charge refunded successfully: %s", charge_details)
        return charge_details
    except Exception as e:
        logger.error("Error refunding charge: %s", e)
        raise PaymentServiceError("Failed to refund charge") from e