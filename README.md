# WhatsApp Cloud API Webhook Service

Production-ready FastAPI backend service for handling Meta WhatsApp Cloud API webhooks.

## Features

- ✅ FastAPI webhook endpoints (GET/POST)
- ✅ Webhook signature verification (X-Hub-Signature-256)
- ✅ Async database operations with SQLAlchemy
- ✅ PostgreSQL storage for events and messages
- ✅ Structured JSON logging with Loguru
- ✅ Docker and Docker Compose support
- ✅ Database migrations with Alembic
- ✅ Pydantic v2 validation
- ✅ Unit tests with pytest
- ✅ Health check endpoint
- ✅ Clean architecture with service layer

## Technology Stack

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Loguru
- Docker

## Project Structure

```
whatsapp_listener/
├── app/
│   ├── api/
│   │   └── webhook.py          # Webhook endpoints
│   ├── core/
│   │   ├── config.py           # Configuration
│   │   ├── security.py         # Signature verification
│   │   └── logging.py          # Logging setup
│   ├── db/
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── session.py          # Database session
│   │   └── migrations/         # Alembic migrations
│   ├── schemas/
│   │   └── webhook.py          # Pydantic schemas
│   ├── services/
│   │   └── webhook_processor.py # Business logic
│   └── main.py                 # Application entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

### 1. Clone and Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Configure Environment Variables

```env
# WhatsApp API
VERIFY_TOKEN=your_secure_verify_token
APP_SECRET=your_whatsapp_app_secret

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/whatsapp_webhooks
```

### 3. Run with Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop services
docker-compose down
```

The service will be available at `http://localhost:8000`

### 4. Run Locally (Development)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start application
python -m app.main
```

## Database Setup

### Run Migrations

```bash
# Upgrade to latest version
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Generate new migration
alembic revision --autogenerate -m "description"
```

### Database Schema

**webhook_events** - Stores raw webhook payloads
- id (PK)
- event_type
- payload_json
- received_at

**whatsapp_messages** - Stores parsed messages
- id (PK)
- wamid (unique)
- phone_number
- direction (incoming/outgoing)
- message_type
- message_text
- timestamp
- status

**message_status_updates** - Stores message status changes
- id (PK)
- wamid
- status
- timestamp
- error_code
- error_message

## API Endpoints

### GET /webhook
Webhook verification endpoint for Meta WhatsApp Cloud API.

**Query Parameters:**
- `hub.mode`: "subscribe"
- `hub.verify_token`: Your verification token
- `hub.challenge`: Challenge string from Meta

**Response:** Returns the challenge string

### POST /webhook
Receives webhook events from Meta WhatsApp Cloud API.

**Headers:**
- `X-Hub-Signature-256`: Webhook signature for verification

**Request Body:** JSON webhook payload from Meta

**Response:**
```json
{
  "status": "received"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "WhatsApp Webhook Service",
  "version": "1.0.0"
}
```

## Meta WhatsApp Setup

### 1. Configure Webhook URL

In your Meta App Dashboard:

1. Go to WhatsApp > Configuration
2. Set Webhook URL: `https://your-domain.com/webhook`
3. Set Verify Token: Same as `VERIFY_TOKEN` in your .env
4. Subscribe to webhook fields:
   - messages
   - message_status

### 2. Get App Secret

1. Go to App Settings > Basic
2. Copy your App Secret
3. Add to .env as `APP_SECRET`

## Testing

### Run Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest test_webhook.py::test_webhook_verification_success
```

### Manual Testing

Test webhook verification:
```bash
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=your_token&hub.challenge=test123"
```

Test webhook reception (with signature):
```bash
python -c "
import hmac
import hashlib
import json

payload = {'object': 'whatsapp_business_account', 'entry': []}
payload_str = json.dumps(payload)
secret = 'your_app_secret'
sig = hmac.new(secret.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
print(f'Signature: sha256={sig}')
"

curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=YOUR_SIGNATURE" \
  -d '{"object":"whatsapp_business_account","entry":[]}'
```

## Monitoring and Logs

### View Logs

```bash
# Docker
docker-compose logs -f app

# Local
# Logs output to stdout with JSON formatting in production
```

### Log Structure

```json
{
  "time": "2024-01-01 12:00:00",
  "level": "INFO",
  "message": "Request: POST /webhook"
}
```

## Security Considerations

1. **Signature Verification**: All webhook requests are verified using HMAC-SHA256
2. **Environment Variables**: Sensitive data stored in environment variables
3. **HTTPS Required**: Use HTTPS in production (handled by reverse proxy)
4. **Database Security**: Use strong passwords and connection pooling
5. **Error Handling**: Errors logged but not exposed to clients

## Production Deployment

### With Docker

```bash
# Build image
docker build -t whatsapp-webhook:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  whatsapp-webhook:latest
```

### With Reverse Proxy (Nginx)

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Environment Variables for Production

```env
ENVIRONMENT=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://user:password@db-host:5432/dbname
```

## Troubleshooting

### Webhook Verification Fails
- Ensure `VERIFY_TOKEN` matches the token configured in Meta dashboard
- Check webhook URL is accessible from internet

### Signature Verification Fails
- Verify `APP_SECRET` matches your Meta App Secret
- Ensure request body is not modified before verification

### Database Connection Issues
- Check `DATABASE_URL` format
- Ensure PostgreSQL is running
- Verify network connectivity to database

### Messages Not Storing
- Check application logs for errors
- Verify database migrations ran successfully
- Test database connectivity

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT

## Support

For issues related to:
- **This service**: Check logs and troubleshooting section
- **Meta WhatsApp API**: Refer to [Meta Developer Documentation](https://developers.facebook.com/docs/whatsapp)
