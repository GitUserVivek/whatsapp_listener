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
    print(f"Webhook verification: mode={mode}")
    return challenge


@router.post("/webhook")
async def receive_webhook(request: Request):
    """Receive and log webhook events"""
    payload = await request.json()
    
    # Parse and log status updates
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            
            # Handle status updates
            if "statuses" in value:
                for status in value["statuses"]:
                    print(
                        f"Status Update | "
                        f"ID: {status.get('id')} | "
                        f"Status: {status.get('status')} | "
                        f"Recipient: {status.get('recipient_id')} | "
                        f"Timestamp: {status.get('timestamp')} | "
                        f"Conversation: {status.get('conversation', {}).get('id')}"
                    )
            
            # Handle incoming messages
            if "messages" in value:
                for message in value["messages"]:
                    print(
                        f"Message | "
                        f"ID: {message.get('id')} | "
                        f"From: {message.get('from')} | "
                        f"Type: {message.get('type')} | "
                        f"Timestamp: {message.get('timestamp')}"
                    )
    
    return {"status": "received"}
