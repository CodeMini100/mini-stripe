"""Pydantic models for validating webhook payloads if needed."""

from pydantic import BaseModel, Field
from typing import Optional, Dict


class WebhookEvent(BaseModel):
    """
    Model representing the event portion of a webhook payload.
    This class can be extended to include additional fields or validations.
    """

    event_id: str = Field(..., description="Unique identifier of the webhook event.")
    event_type: str = Field(..., description="Type of the webhook event.")
    # TODO: Add more fields as needed


class WebhookPayload(BaseModel):
    """
    Model representing the complete payload received from a webhook.
    This class can be extended to include additional fields or validations.
    """

    event: WebhookEvent = Field(..., description="The event associated with this payload.")
    data: Optional[Dict[str, str]] = Field(None, description="Additional data related to the event.")
    # TODO: Add more fields as needed