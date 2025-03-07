import motor.motor_asyncio
from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorCollection

client = motor.motor_asyncio.AsyncIOMotorClient(get_settings().MONGODB_URL)
db = client["tori-db"]
