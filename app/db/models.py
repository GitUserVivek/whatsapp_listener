from datetime import datetime
from sqlalchemy import Text, String, JSON, DateTime, Integer, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
import enum


class Base(DeclarativeBase):
    pass


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        index=True
    )


class MessageDirection(enum.Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wamid: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    direction: Mapped[MessageDirection] = mapped_column(Enum(MessageDirection), nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), nullable=False)
    message_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)


class MessageStatusUpdate(Base):
    __tablename__ = "message_status_updates"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wamid: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    error_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
