from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    FRONTEND_URL: str
    
    # ML Models
    MODEL_PATH: str = "./models/xgboost_model.pkl"
    PREPROCESSOR_PATH: str = "./models/preprocessor.pkl"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
