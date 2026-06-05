import hmac
import hashlib
from fastapi import HTTPException, status


def verify_webhook_signature(payload: bytes, signature: str, app_secret: str) -> bool:
    """
    Verify webhook signature from Meta.
    X-Hub-Signature-256 header format: sha256=<signature>
    """
    if not signature:
        return False
    
    try:
        signature_method, signature_hash = signature.split("=", 1)
        if signature_method != "sha256":
            return False
    except ValueError:
        return False
    
    expected_signature = hmac.new(
        app_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_hash)


def validate_signature_header(payload: bytes, signature: str | None, app_secret: str) -> None:
    """Validate signature or raise HTTPException"""
    if not signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature header"
        )
    
    if not verify_webhook_signature(payload, signature, app_secret):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid signature"
        )
