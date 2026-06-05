from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WhatsApp Webhook Service"
    app_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"


settings = Settings()
