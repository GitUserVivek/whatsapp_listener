import sys
from loguru import logger
from app.core.config import settings


def configure_logging() -> None:
    """Configure structured JSON logging with loguru"""
    logger.remove()
    
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=settings.log_level,
        serialize=True if settings.environment == "production" else False,
        backtrace=True,
        diagnose=settings.environment != "production",
    )
