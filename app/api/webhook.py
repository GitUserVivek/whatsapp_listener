from fastapi import APIRouter, Request, Response, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.core.config import settings
from app.core.security import validate_signature_header
from app.db.session import get_db
from app.services.webhook_processor import WebhookProcessor

router = APIRouter(tags=["webhook"])


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge"),
) -> Response:
    """
    Webhook verification endpoint for Meta WhatsApp Cloud API.
    Meta will call this endpoint to verify the webhook URL.
    """
    logger.info(f"Webhook verification request: mode={mode}, token={token[:5]}...")
    
    if mode == "subscribe" and token == settings.verify_token:
        logger.info("Webhook verified successfully")
        return Response(content=challenge, media_type="text/plain")
    
    logger.warning("Webhook verification failed: invalid token")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification token mismatch"
    )


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def receive_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """
    Receive webhook events from Meta WhatsApp Cloud API.
    Validates signature, stores event, and processes asynchronously.
    """
    # Get raw body for signature verification
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    
    # Verify signature
    validate_signature_header(body, signature, settings.app_secret)
    
    # Parse JSON payload
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Invalid JSON payload: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON payload"
        )
    
    logger.info(f"Received webhook event: {payload.get('object')}")
    
    # Process webhook
    processor = WebhookProcessor(db)
    
    try:
        await processor.process_webhook(payload)
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        # Still return 200 to avoid retries from Meta
        # Log the error for manual investigation
    
    return {"status": "received"}
