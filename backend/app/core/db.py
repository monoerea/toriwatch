from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import get_settings

class Database:
    """Manages MongoDB connection for multiple clients."""
    def __init__(self, db_name: str = "tori-db"):
        self.db_name = db_name
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def connect(self):
        """Initialize a new database connection."""
        self.client = AsyncIOMotorClient(get_settings().MONGODB_URL)
        self.db = self.client[self.db_name]

    async def close(self):
        """Close the database connection."""
        if self.client:
            self.client.close()

    def get_db(self) -> AsyncIOMotorDatabase:
        """Retrieve the database instance."""
        if not self.db:
            raise RuntimeError("Database is not initialized. Call connect() first.")
        return self.db
