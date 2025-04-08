from typing import Any, Dict
import logging

from fastapi import APIRouter, Request, HTTPException, status

router = APIRouter()


def webhook_receiver_endpoint(request_data: Dict[str, Any], headers: Dict[str, str]) -> None:
    """
    Validates the signature and routes the event to the relevant handler.

    :param request_data: The JSON payload from the webhook event.
    :param headers: The HTTP headers from the request.
    :raises HTTPException: If signature validation fails or an event type is unsupported.
    """
    # TODO: Implement signature validation
    # signature = headers.get("X-Signature", "")
    # if not valid_signature(signature, request_data):
    #     raise HTTPException(status_code=400, detail="Invalid signature")

    # TODO: Route event to relevant handler
    # event_type = request_data.get("event_type")
    # if event_type == "some_event":
    #     handle_some_event(request_data)
    # else:
    #     raise HTTPException(status_code=400, detail="Unsupported event type")

    pass  # Remove once implemented


@router.post("/webhook")
async def receive_webhook(request: Request) -> Dict[str, str]:
    """
    FastAPI endpoint to receive webhook events.

    :param request: The incoming request object.
    :return: A dictionary indicating the result of the webhook processing.
    :raises HTTPException: If validation or processing fails.
    """
    try:
        data = await request.json()
        hdrs = dict(request.headers)
        webhook_receiver_endpoint(data, hdrs)
        return {"status": "success", "message": "Webhook received successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        logging.exception("Error while processing webhook")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        ) from exc