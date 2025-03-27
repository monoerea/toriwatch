import logging
import os
from fastapi import FastAPI
from app.api.router import api_router
from app.core.logger import logger
from contextlib import asynccontextmanager
from app.core.config import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(level=settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Starting {settings.APP_NAME} - Version {settings.VERSION}")

    yield

    logger.info(f"🛑 Shutting down {settings.APP_NAME} - Version {settings.VERSION}")

app = FastAPI(lifespan=lifespan, title=settings.APP_NAME, version=settings.VERSION, summary=settings.SUMMARY, root_path=settings.ROOT_PATH)

app.include_router(api_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

@app.get("/settings")
async def get_config():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
    }
