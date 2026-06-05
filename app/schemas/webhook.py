from pydantic import BaseModel, Field
from typing import Any


# Webhook verification
class WebhookVerification(BaseModel):
    hub_mode: str = Field(alias="hub.mode")
    hub_verify_token: str = Field(alias="hub.verify_token")
    hub_challenge: str = Field(alias="hub.challenge")


# WhatsApp webhook payload models
class Profile(BaseModel):
    name: str


class Contact(BaseModel):
    profile: Profile
    wa_id: str


class TextMessage(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: TextMessage | None = None


class MessageStatus(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    errors: list[dict[str, Any]] | None = None


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: list[Contact] | None = None
    messages: list[Message] | None = None
    statuses: list[MessageStatus] | None = None


class Change(BaseModel):
    value: Value
    field: str


class Entry(BaseModel):
    id: str
    changes: list[Change]


class WebhookPayload(BaseModel):
    object: str
    entry: list[Entry]
