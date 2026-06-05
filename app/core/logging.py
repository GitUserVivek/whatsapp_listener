import sys
from loguru import logger
from app.core.config import settings


def configure_logging() -> None:
    """Configure logging with loguru"""
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=settings.log_level,
    )
