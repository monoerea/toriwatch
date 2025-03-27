from typing import AsyncGenerator
from app.core.db import Database
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """Dependency to provide a MongoDB database instance."""
    db_instance = Database()
    await db_instance.connect()
    try:
        yield db_instance.get_db()
    finally:
        await db_instance.close()