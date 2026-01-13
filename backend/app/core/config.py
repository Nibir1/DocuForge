import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """
    Application Settings Configuration.
    
    Validates environment variables on startup.
    Uses Pydantic v2 SettingsConfigDict for .env file loading.
    """
    
    # Project Info
    PROJECT_NAME: str = "DocuForge"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "production"] = "dev"
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL_ID: str = "gpt-4-turbo-preview"
    
    # Qdrant Vector DB Settings
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333

    # Configuration to read from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignore extra vars in .env that aren't defined here
    )

# Singleton instance
settings = Settings()