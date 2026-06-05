# Example Meta WhatsApp Cloud API Webhook Payloads

## 1. Incoming Text Message

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15551234567",
          "phone_number_id": "123456789"
        },
        "contacts": [{
          "profile": {
            "name": "John Doe"
          },
          "wa_id": "15559876543"
        }],
        "messages": [{
          "from": "15559876543",
          "id": "wamid.HBgNMTU1NTk4NzY1NDMVAgARGBI5QTNDQTU2N0Q1RjhBMEQ3OTMA",
          "timestamp": "1234567890",
          "type": "text",
          "text": {
            "body": "Hello, World!"
          }
        }]
      },
      "field": "messages"
    }]
  }]
}
```

## 2. Message Status Update - Delivered

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15551234567",
          "phone_number_id": "123456789"
        },
        "statuses": [{
          "id": "wamid.HBgNMTU1NTk4NzY1NDMVAgARGBI5QTNDQTU2N0Q1RjhBMEQ3OTMA",
          "status": "delivered",
          "timestamp": "1234567890",
          "recipient_id": "15559876543"
        }]
      },
      "field": "messages"
    }]
  }]
}
```

## 3. Message Status Update - Read

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15551234567",
          "phone_number_id": "123456789"
        },
        "statuses": [{
          "id": "wamid.HBgNMTU1NTk4NzY1NDMVAgARGBI5QTNDQTU2N0Q1RjhBMEQ3OTMA",
          "status": "read",
          "timestamp": "1234567890",
          "recipient_id": "15559876543"
        }]
      },
      "field": "messages"
    }]
  }]
}
```

## 4. Message Status Update - Failed

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15551234567",
          "phone_number_id": "123456789"
        },
        "statuses": [{
          "id": "wamid.HBgNMTU1NTk4NzY1NDMVAgARGBI5QTNDQTU2N0Q1RjhBMEQ3OTMA",
          "status": "failed",
          "timestamp": "1234567890",
          "recipient_id": "15559876543",
          "errors": [{
            "code": 131047,
            "title": "Re-engagement message",
            "message": "Re-engagement message"
          }]
        }]
      },
      "field": "messages"
    }]
  }]
}
```

## 5. Incoming Image Message

```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "15551234567",
          "phone_number_id": "123456789"
        },
        "contacts": [{
          "profile": {
            "name": "John Doe"
          },
          "wa_id": "15559876543"
        }],
        "messages": [{
          "from": "15559876543",
          "id": "wamid.HBgNMTU1NTk4NzY1NDMVAgARGBI5QTNDQTU2N0Q1RjhBMEQ3OTMA",
          "timestamp": "1234567890",
          "type": "image",
          "image": {
            "mime_type": "image/jpeg",
            "sha256": "IMAGE_HASH",
            "id": "IMAGE_ID"
          }
        }]
      },
      "field": "messages"
    }]
  }]
}
```
