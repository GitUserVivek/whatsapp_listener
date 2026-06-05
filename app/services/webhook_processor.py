from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger
from app.db.models import WebhookEvent, WhatsAppMessage, MessageStatusUpdate, MessageDirection
from app.schemas.webhook import WebhookPayload, Message, MessageStatus
from typing import Any


class WebhookProcessor:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def process_webhook(self, payload: dict) -> None:
        """Process incoming webhook and store events"""
        try:
            validated_payload = WebhookPayload(**payload)
            
            # Store raw webhook event
            await self._store_webhook_event("whatsapp_webhook", payload)
            
            # Process each entry
            for entry in validated_payload.entry:
                for change in entry.changes:
                    if change.field == "messages":
                        await self._process_messages(change.value)
            
            logger.info("Webhook processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            raise
    
    async def _store_webhook_event(self, event_type: str, payload: dict) -> None:
        """Store raw webhook event"""
        event = WebhookEvent(
            event_type=event_type,
            payload_json=payload
        )
        self.db.add(event)
        await self.db.flush()
    
    async def _process_messages(self, value: Any) -> None:
        """Process incoming messages and status updates"""
        # Process incoming messages
        if value.messages:
            for message in value.messages:
                await self._store_incoming_message(message)
        
        # Process status updates
        if value.statuses:
            for status in value.statuses:
                await self._store_status_update(status)
    
    async def _store_incoming_message(self, message: Message) -> None:
        """Store incoming WhatsApp message"""
        try:
            # Check if message already exists
            stmt = select(WhatsAppMessage).where(WhatsAppMessage.wamid == message.id)
            result = await self.db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if existing:
                logger.debug(f"Message {message.id} already exists")
                return
            
            message_text = message.text.body if message.text else None
            
            wa_message = WhatsAppMessage(
                wamid=message.id,
                phone_number=message.from_,
                direction=MessageDirection.INCOMING,
                message_type=message.type,
                message_text=message_text,
                timestamp=datetime.fromtimestamp(int(message.timestamp)),
                status="received"
            )
            
            self.db.add(wa_message)
            await self.db.flush()
            
            logger.info(f"Stored incoming message: {message.id}")
            
        except Exception as e:
            logger.error(f"Error storing message {message.id}: {e}")
            raise
    
    async def _store_status_update(self, status: MessageStatus) -> None:
        """Store message status update"""
        try:
            error_code = None
            error_message = None
            
            if status.errors:
                error_code = status.errors[0].get("code")
                error_message = status.errors[0].get("title")
            
            status_update = MessageStatusUpdate(
                wamid=status.id,
                status=status.status,
                timestamp=datetime.fromtimestamp(int(status.timestamp)),
                error_code=error_code,
                error_message=error_message
            )
            
            self.db.add(status_update)
            await self.db.flush()
            
            # Update message status if exists
            stmt = select(WhatsAppMessage).where(WhatsAppMessage.wamid == status.id)
            result = await self.db.execute(stmt)
            message = result.scalar_one_or_none()
            
            if message:
                message.status = status.status
                await self.db.flush()
            
            logger.info(f"Stored status update for message: {status.id} - {status.status}")
            
        except Exception as e:
            logger.error(f"Error storing status update {status.id}: {e}")
            raise
