from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./aura_dev.db"
    
    # JWT
    SECRET_KEY: str = "default-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Support both local and production
    FRONTEND_URL: str = "http://localhost:3000"
    
    # ML Models - Use relative paths that work in both local and production
    MODEL_PATH: str = "./models/best_model.pkl"
    PREPROCESSOR_PATH: str = "./models/preprocessor.pkl"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
