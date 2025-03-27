import sys
import os
# Ensure correct module path resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
import motor.motor_asyncio
from bson import ObjectId
from fastapi import HTTPException
from app.repositories.user import UserRepository
from app.services.users import UserService
from app.model.users import User, UserCreate, UserUpdate, UpdateAccountClassification
from app.core.config import get_settings 


@pytest.fixture(scope="module")
def test_db():
    """Creates a test database connection"""
    client = motor.motor_asyncio.AsyncIOMotorClient(get_settings().MONGODB_URL, tls=True, tlsAllowInvalidCertificates=True)
    db = client["tori-db"]  # Use a test database
    yield db  # Correct fixture syntax for test database

@pytest.fixture(scope="module")
def user_repo(test_db):
    """Creates a UserRepository with the test DB"""
    return UserRepository(test_db)  # Correct repository initialization

@pytest.fixture(scope="module")
def user_service(test_db):
    """Creates a UserService with the test DB"""
    return UserService(test_db)  # Pass the database, not the repo

@pytest.mark.asyncio
async def test_create_user(user_service):
    """Test creating a user in the actual MongoDB"""
    user_data = UserCreate(
    xid=98765432,
    username="test_user",
    email="testuser@example.com",
    password="securepassword",
    twitter_access_token="sample_token",
    twitter_access_token_secret="sample_token_secret",
    account_classification="bot",
    has_access=True,
    is_authenticated=False
)


    created_user = await user_service.create_user(user_data)
    
    assert isinstance(created_user, User)
    assert created_user.username == "test_user"
    assert created_user.email == "testuser@example.com"

@pytest.mark.asyncio
async def test_list_users(user_service):
    """Test listing users from the actual MongoDB"""
    users = await user_service.list_users()
    assert users is not None
    assert len(users.users) > 0  # Ensure at least 1 user exists

@pytest.mark.asyncio
async def test_get_user(user_service):
    """Test retrieving a user by ID"""
    users = await user_service.list_users()
    user_id = users.users[0].id

    user = await user_service.get_user(user_id)
    assert user.id == user_id

@pytest.mark.asyncio
async def test_update_user(user_service):
    """Test updating a user in MongoDB"""
    users = await user_service.list_users()
    user_id = users.users[0].id

    user_update = UserUpdate(username="updated_user")
    account_classification = UpdateAccountClassification(label="bot", confidence_score=0.95)

    updated_user = await user_service.update_user(user_id, user_update, account_classification)

    assert updated_user.username == "updated_user"

@pytest.mark.asyncio
async def test_delete_user(user_service):
    """Test deleting a user from MongoDB"""
    users = await user_service.list_users()
    user_id = users.users[0].id

    await user_service.delete_user(user_id)

    with pytest.raises(HTTPException) as exc_info:
        await user_service.get_user(user_id)
    assert exc_info.value.status_code == 404
