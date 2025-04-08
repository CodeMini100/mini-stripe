import requests
from typing import Any, Dict

# TODO: Update BASE_URL to point to the actual Stripe_lite FastAPI service
BASE_URL = "http://localhost:8000"


def create_charge(customer_id: str, amount: int, payment_method: str) -> Dict[str, Any]:
    """
    Sends a POST request to /payments/create_charge.

    Args:
        customer_id (str): The ID of the customer to be charged.
        amount (int): The amount to charge in the smallest currency unit (e.g., cents).
        payment_method (str): The identifier for the payment method.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the request.
    """
    # TODO: Implement authentication if needed
    url = f"{BASE_URL}/payments/create_charge"
    payload = {
        "customer_id": customer_id,
        "amount": amount,
        "payment_method": payment_method
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        # TODO: Log the error and handle it appropriately
        raise exc


def refund_charge(charge_id: str) -> Dict[str, Any]:
    """
    Sends a POST request to /payments/refund_charge.

    Args:
        charge_id (str): The ID of the charge to refund.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the request.
    """
    # TODO: Implement authentication if needed
    url = f"{BASE_URL}/payments/refund_charge"
    payload = {
        "charge_id": charge_id
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        # TODO: Log the error and handle it appropriately
        raise exc


def list_customers() -> Dict[str, Any]:
    """
    Example GET request to /customers endpoint.

    Returns:
        Dict[str, Any]: The JSON response from the server.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the request.
    """
    # TODO: Implement authentication if needed
    url = f"{BASE_URL}/customers"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        # TODO: Log the error and handle it appropriately
        raise exc