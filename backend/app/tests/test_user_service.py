import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from app.services.users import UserService
from app.model.users import UserCollection, UserCreate, UserUpdate, UpdateAccountClassification
from app.core.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture
def db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client["users"]

@pytest.fixture
def user_service(db):
    return UserService(db())

@pytest.mark.asyncio
async def test_list_users(user_service):
    users = await user_service.list_users()
    assert isinstance(users, UserCollection)

@pytest.mark.asyncio
async def test_create_user_service(user_service):
    user_data = UserCreate(name="Test User", email="test@example.com")
    user = await user_service.create_user(user_data)
    assert user.name == "Test User"

@pytest.mark.asyncio
async def test_get_user(user_service):
    user_id = "some_user_id"
    user = await user_service.get_user(user_id)
    assert user is None or user.id == user_id

@pytest.mark.asyncio
async def test_update_user(user_service):
    user_id = "some_user_id"
    user_data = UserUpdate(name="Updated User")
    account_classification = UpdateAccountClassification(label="test", confidence_score=0.9)
    user = await user_service.update_user(user_id, user_data, account_classification)
    assert user is None or user.name == "Updated User"

@pytest.mark.asyncio
async def test_delete_user(user_service):
    user_id = id
    result = await user_service.delete_user(user_id)
    assert result is None