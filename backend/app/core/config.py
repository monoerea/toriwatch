from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(r"C:\Users\senor\Documents\x-bot-spt-ext\backend\.env")
load_dotenv(env_path)


class Settings(BaseSettings):
    APP_NAME: str = "X-Bot API"
    VERSION: str = "1.0.0"
    SUMMARY: str = "A backend for a X Bot Detector chrome extension"
    API_PREFIX: str = "/api"

    MONGODB_URL: str = os.getenv("MONGODB_URL")

    DEBUG: bool = True  # Toggle debug mode
    SECRET_KEY: str  # For security (JWT, hashing)
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    class Config:
        env_file = ".env"  # Load from a .env file
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()
