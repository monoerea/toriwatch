import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://sheensenorin:CJEl8tFLYP5fLPIF@tori-db.vo3pe.mongodb.net/")
db = client["tori-db"]
user_collection = db.get_collection("users")

# Test the connection
async def test_connection():
    try:
        # Check if we can find any users
        user = await user_collection.find_one({})
        print("User found:", user)
    except Exception as e:
        print("Error connecting to MongoDB:", e)

import asyncio
asyncio.run(test_connection())
