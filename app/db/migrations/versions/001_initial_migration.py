"""Initial migration - create webhook tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create webhook_events table
    op.create_table(
        'webhook_events',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('payload_json', sa.JSON(), nullable=False),
        sa.Column('received_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webhook_events_event_type'), 'webhook_events', ['event_type'], unique=False)
    op.create_index(op.f('ix_webhook_events_received_at'), 'webhook_events', ['received_at'], unique=False)
    
    # Create whatsapp_messages table
    op.create_table(
        'whatsapp_messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wamid', sa.String(length=255), nullable=False),
        sa.Column('phone_number', sa.String(length=50), nullable=False),
        sa.Column('direction', sa.Enum('INCOMING', 'OUTGOING', name='messagedirection'), nullable=False),
        sa.Column('message_type', sa.String(length=50), nullable=False),
        sa.Column('message_text', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('wamid')
    )
    op.create_index(op.f('ix_whatsapp_messages_wamid'), 'whatsapp_messages', ['wamid'], unique=True)
    op.create_index(op.f('ix_whatsapp_messages_phone_number'), 'whatsapp_messages', ['phone_number'], unique=False)
    op.create_index(op.f('ix_whatsapp_messages_timestamp'), 'whatsapp_messages', ['timestamp'], unique=False)
    
    # Create message_status_updates table
    op.create_table(
        'message_status_updates',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wamid', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('error_code', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_status_updates_wamid'), 'message_status_updates', ['wamid'], unique=False)
    op.create_index(op.f('ix_message_status_updates_timestamp'), 'message_status_updates', ['timestamp'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_message_status_updates_timestamp'), table_name='message_status_updates')
    op.drop_index(op.f('ix_message_status_updates_wamid'), table_name='message_status_updates')
    op.drop_table('message_status_updates')
    
    op.drop_index(op.f('ix_whatsapp_messages_timestamp'), table_name='whatsapp_messages')
    op.drop_index(op.f('ix_whatsapp_messages_phone_number'), table_name='whatsapp_messages')
    op.drop_index(op.f('ix_whatsapp_messages_wamid'), table_name='whatsapp_messages')
    op.drop_table('whatsapp_messages')
    
    op.drop_index(op.f('ix_webhook_events_received_at'), table_name='webhook_events')
    op.drop_index(op.f('ix_webhook_events_event_type'), table_name='webhook_events')
    op.drop_table('webhook_events')
    
    sa.Enum('INCOMING', 'OUTGOING', name='messagedirection').drop(op.get_bind())
