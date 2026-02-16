"""Configuration management for the application."""
import os
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""
    
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "dockerized-api")
    ENV: str = os.getenv("ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    GIT_SHA: Optional[str] = os.getenv("GIT_SHA", None)
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENV.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENV.lower() == "development"


settings = Settings()
