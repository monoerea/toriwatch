from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import get_settings
from app.core.logger import logger

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# Attach API router
app.include_router(api_router)

# Run Startup Event
@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Starting {settings.APP_NAME} - Version {settings.VERSION}")

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}
