from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import get_settings
from app.core.logger import logger
from contextlib import asynccontextmanager
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Starting {settings.APP_NAME} - Version {settings.VERSION}")

    yield

    logger.info(f"🛑 Shutting down {settings.APP_NAME} - Version {settings.VERSION}")
app = FastAPI(lifespan=lifespan, title=settings.APP_NAME, version=settings.VERSION, summary=settings.SUMMARY)

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
