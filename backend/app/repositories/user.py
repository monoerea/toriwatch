import asyncio
from bson import ObjectId
from pymongo import ReturnDocument
from fastapi import HTTPException, status
from app.core.db import db

async def list_users() -> list[dict]:
    """Fetch all users from the database."""
    try:
        users = await db['users'].find().to_list(length=None)
        return users if users else []
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_user_by_id(user_id: str) -> dict:
    """Fetch a user by ID with error handling."""
    try:
        user = await db['users'].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def create_user(user_data) -> dict:
    """Create a new user in the database."""
    try:
        if asyncio.iscoroutine(user_data):
            user_data = await user_data

        if not isinstance(user_data, dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data format")

        user_data["_id"] = ObjectId()
        new_user = await db['users'].insert_one(user_data)
        created_user = await db['users'].find_one({"_id": new_user.inserted_id})

        if not created_user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")

        return created_user

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



async def update_user(user_id: str, update_data: dict) -> dict:
    """Update user information."""
    try:
        updated_user = await db['users'].find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": update_data}, return_document=ReturnDocument.AFTER
        )
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_user(user_id: str) -> bool:
    """Delete a user."""
    try:
        delete_result = await db['users'].delete_one({"_id": ObjectId(user_id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
