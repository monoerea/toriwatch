from pymongo import ReturnDocument
from fastapi import HTTPException, status
from app.core.db import db

async def insert_user_tokens(user_id: str, access_token: str, access_token_secret: str) -> dict:
    """Insert Twitter authentication tokens for a user."""
    try:
        new_user = {
            "user_id": user_id,
            "access_token": access_token,
            "access_token_secret": access_token_secret
        }
        result = await db['users'].insert_one(new_user)
        if result.inserted_id:
            return new_user
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to insert user tokens")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_user_tokens(user_id: str) -> dict:
    """Retrieve stored Twitter authentication tokens."""
    try:
        user_tokens = await db['users'].find_one({"user_id": user_id})
        if not user_tokens:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tokens for user {user_id} not found")
        return user_tokens
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_user_by_token(access_token: str) -> str | None:
    """Find a user ID by their Twitter access token."""
    try:
        user = await db['users'].find_one({"access_token": access_token})
        return user["user_id"] if user else None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_user_tokens(user_id: str) -> bool:
    """Remove stored Twitter tokens for a user."""
    try:
        delete_result = await db['users'].delete_one({"user_id": user_id})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tokens for user {user_id} not found")
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def update_user_tokens(user_id: str, access_token: str, access_token_secret: str) -> dict:
    """Update Twitter authentication tokens for a user."""
    try:
        updated_user = await db['users'].find_one_and_update(
            {"user_id": user_id},
            {"$set": {"access_token": access_token, "access_token_secret": access_token_secret}},
            return_document=ReturnDocument.AFTER
        )
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
