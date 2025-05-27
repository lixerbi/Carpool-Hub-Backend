from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./carpool_hub.db"

    # Update these default values:
    google_maps_api_key: str = "AIzaSyCJT3FV9SH-5Ln1ooMmWDi-XO_r13OVYqA"
    
    # If using Firebase:
    firebase_api_key: str = "AIzaSyDpd11QLQi8uk-ffF6GU1lsVPoXri7HWcE"
    firebase_project_id: str = "carpool-hub-apis2"
    
    # Keep your existing settings...
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000"]
    
    # App
    app_name: str = "Carpool Hub API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Email (Optional)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
