from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)


class SubscriptionCreateRequest(BaseModel):
    """
    Data required to create a new subscription.
    """
    customer_id: str
    plan_id: str


class SubscriptionResponse(BaseModel):
    """
    Response schema for subscription-related operations.
    """
    subscription_id: str
    customer_id: str
    plan_id: str
    status: str


@router.post("/create", response_model=SubscriptionResponse)
def create_subscription_endpoint(request_data: SubscriptionCreateRequest) -> SubscriptionResponse:
    """
    Subscribes a customer to a plan.

    :param request_data: Data for creating a subscription
    :return: Details of the created subscription
    """
    # TODO: Implement the logic to create a subscription in the database or API
    # Example of error handling:
    try:
        # Example placeholder subscription ID for demonstration
        created_subscription_id = "sub_12345"
        return SubscriptionResponse(
            subscription_id=created_subscription_id,
            customer_id=request_data.customer_id,
            plan_id=request_data.plan_id,
            status="active"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.delete("/{subscription_id}")
def cancel_subscription_endpoint(subscription_id: str) -> dict:
    """
    Cancels an existing subscription.

    :param subscription_id: Unique identifier for the subscription
    :return: Confirmation message or details about the canceled subscription
    """
    # TODO: Implement the logic to cancel the subscription in the database or API
    try:
        # Placeholder logic for demonstration
        return {"message": f"Subscription {subscription_id} has been canceled."}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions_endpoint() -> List[SubscriptionResponse]:
    """
    Lists all subscriptions.

    :return: List of current subscriptions
    """
    # TODO: Implement the logic to list all subscriptions from the database or API
    # Placeholder example:
    return [
        SubscriptionResponse(
            subscription_id="sub_12345",
            customer_id="cust_abc",
            plan_id="plan_gold",
            status="active"
        ),
        SubscriptionResponse(
            subscription_id="sub_67890",
            customer_id="cust_xyz",
            plan_id="plan_silver",
            status="canceled"
        ),
    ]