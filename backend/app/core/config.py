from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
import secrets
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
ENV_PATH = os.path.join(BASE_DIR, "..", "..", "..", ".env")  # Move three levels up

load_dotenv(ENV_PATH)

class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = os.environ.get('PROJECT_NAME','sagemaker-fastapi')
    APP_NAME: str = "X-Bot API"
    VERSION: str = "1.0.0"
    SUMMARY: str = "X Bot Detector chrome extension"
    API_PREFIX: str = "/api"
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DEBUG: bool = True
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL','INFO')
    ROOT_PATH: str = os.environ.get(ENV_PATH)
    REGION: str = os.environ.get('REGION','us-west-2')
    RAW_BUCKET: str = os.environ.get('RAW_BUCKET')
    ARTIFACTS_BUCKET: str = os.environ.get('ARTIFACTS_BUCKET')
    OUTPUT_BUCKET: str = os.environ.get('OUTPUT_BUCKET')
    class Config:
        env_file = ".env"  # Load from a .env file
        env_file_encoding = "utf-8"

settings = Settings()