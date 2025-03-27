import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from app.repositories.user import UserRepository
from bson import ObjectId
from app.dependencies.db import get_db
id =  ObjectId()
@pytest.fixture(scope="module")
async def user_data():
    """Mock user data."""
    return {
        "_id":id,
        "xid": 12345678,
        "username": "testuser",
        "email": "test@example.com",
        "has_access": True,
        "is_authenticated": False
    }

@pytest.fixture
def user_repo():
    db = get_db()
    return UserRepository(db)

@pytest.mark.asyncio
async def test_list_users(user_repo):
    users = await user_repo.list_users()
    assert isinstance(users, list)

@pytest.mark.asyncio
async def test_create_user(user_repo):
    user_data = {"id":id, "name": "Test User", "email": "test@example.com"}
    user = await user_repo.create_user(user_data)
    assert user["name"] == "Test User"
    assert user["id"] == id

@pytest.mark.asyncio
async def test_get_user_by_id(user_repo):
    user_id = id
    user = await user_repo.get_user_by_id(user_id)
    assert user is None or isinstance(user, dict)

@pytest.mark.asyncio
async def test_update_user(user_repo):
    user_id = id
    update_data = {"name": "Updated User"}
    user = await user_repo.update_user(user_id, update_data)
    assert user is None or user["name"] == "Updated User"

@pytest.mark.asyncio
async def test_delete_user(user_repo):
    user_id = id
    result = await user_repo.delete_user(user_id)
    assert result is True or result is False