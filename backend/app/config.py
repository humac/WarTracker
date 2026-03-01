from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "WarTracker"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://wartracker:changeme@localhost:5432/wartracker")
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "change-this-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "https://wartracker.org",
        "https://www.wartracker.org",
    ]
    
    # Rate Limiting
    RATE_LIMIT_PER_HOUR: int = 100
    
    # Ollama AI
    OLLAMA_API_URL: str = "http://localhost:11434"
    OLLAMA_MODEL_SUMMARY: str = "qwen3.5:397b-cloud"
    OLLAMA_MODEL_CLASSIFICATION: str = "glm-5:cloud"
    
    # Data Sources (API keys)
    GDELT_API_URL: Optional[str] = None
    ACLED_API_KEY: Optional[str] = None
    NEWSAPI_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
