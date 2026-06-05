import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.models import Base
from app.db.session import get_db
from app.core.config import settings
import hmac
import hashlib

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def db_session():
    """Create test database session"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db_session):
    """Create test client with database session override"""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


def create_signature(payload: str, secret: str) -> str:
    """Create webhook signature"""
    signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


@pytest.mark.asyncio
async def test_webhook_verification_success(client: AsyncClient):
    """Test successful webhook verification"""
    response = await client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": settings.verify_token,
            "hub.challenge": "test_challenge_123"
        }
    )
    
    assert response.status_code == 200
    assert response.text == "test_challenge_123"


@pytest.mark.asyncio
async def test_webhook_verification_failure(client: AsyncClient):
    """Test webhook verification with wrong token"""
    response = await client.get(
        "/webhook",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "wrong_token",
            "hub.challenge": "test_challenge_123"
        }
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_webhook_receive_valid_message(client: AsyncClient):
    """Test receiving a valid webhook message"""
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123456",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "1234567890",
                        "phone_number_id": "123456789"
                    },
                    "messages": [{
                        "from": "1234567890",
                        "id": "wamid.123456",
                        "timestamp": "1234567890",
                        "type": "text",
                        "text": {
                            "body": "Hello World"
                        }
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    payload_str = str(payload).replace("'", '"')
    signature = create_signature(payload_str, settings.app_secret)
    
    response = await client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": signature}
    )
    
    assert response.status_code == 200
    assert response.json() == {"status": "received"}


@pytest.mark.asyncio
async def test_webhook_invalid_signature(client: AsyncClient):
    """Test webhook with invalid signature"""
    payload = {"object": "whatsapp_business_account", "entry": []}
    
    response = await client.post(
        "/webhook",
        json=payload,
        headers={"X-Hub-Signature-256": "sha256=invalid"}
    )
    
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint"""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data
