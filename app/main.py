from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from app.core.config import settings
from app.core.logging import configure_logging
from app.api.webhook import router as webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    configure_logging()
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }


app.include_router(webhook_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
