from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    # Application
    app_name: str = "WhatsApp Webhook Service"
    app_version: str = "1.0.0"
    environment: str = "production"
    
    # WhatsApp API
    verify_token: str
    app_secret: str
    
    # Database
    database_url: str
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"


settings = Settings()
