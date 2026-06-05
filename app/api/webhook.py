from fastapi import APIRouter, Request, Query
from loguru import logger

router = APIRouter(tags=["webhook"])


@router.get("/webhook")
async def verify_webhook(
    mode: str = Query(alias="hub.mode"),
    token: str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge"),
):
    """Webhook verification endpoint"""
    logger.info(f"Webhook verification: mode={mode}")
    return challenge


@router.post("/webhook")
async def receive_webhook(request: Request):
    """Receive and log webhook events"""
    payload = await request.json()
    logger.info(f"Webhook received: {payload}")
    return {"status": "received"}
