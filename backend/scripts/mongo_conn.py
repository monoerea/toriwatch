import ssl
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

# Replace with your actual MongoDB connection URI
MONGODB_URL = "mongodb+srv://sheensenorin:CJEl8tFLYP5fLPIF@tori-db.vo3pe.mongodb.net/"

async def test_mongodb_connection(uri):
    try:
        # Establishing a connection to MongoDB with Motor
        client = AsyncIOMotorClient(uri, ssl=True)
        
        # Testing connection
        await client.admin.command('ping')
        print("MongoDB connection successful!")
    
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection(MONGODB_URL))
