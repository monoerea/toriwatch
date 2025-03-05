from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
ENV_PATH = os.path.join(BASE_DIR, "..", "..", "..", ".env")  # Move three levels up

load_dotenv(ENV_PATH)

class Settings(BaseSettings):
    APP_NAME: str = "X-Bot API"
    VERSION: str = "1.0.0"
    SUMMARY: str = "A backend for a X Bot Detector chrome extension"
    API_PREFIX: str = "/api"

    MONGODB_URL: str = os.getenv("MONGODB_URL")

    DEBUG: bool = True  # Toggle debug mode security (JWT, hashing)
    class Config:
        env_file = ".env"  # Load from a .env file
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()