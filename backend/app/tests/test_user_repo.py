import asyncio
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from app.repositories.user import (
    list_users, get_user_by_id, create_user, update_user, delete_user
)
from bson import ObjectId

@pytest.fixture(scope="module")
async def user_data():
    """Mock user data."""
    return {
        "_id": ObjectId(),
        "xid": 12345678,
        "username": "testuser",
        "email": "test@example.com",
        "has_access": True,
        "is_authenticated": False
    }

@pytest.mark.asyncio
async def test_list_users():
    users = await list_users()
    assert len(users) > 0

@pytest.mark.asyncio
async def test_create_user():
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "has_access": True,
        "is_authenticated": False,
        "account_classification": "bot",
        "created_at": "2024-03-07T12:00:00Z",
        "follower_count": 100,
        "following_count": 50,
        "tweet_count": 200,
        "engagement_score": 0.75
    }

    created_user = await create_user(user_data)
    assert created_user is not None
    assert created_user["email"] == "test@example.com"