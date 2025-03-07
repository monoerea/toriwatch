import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.services.users import list_users_service
from app.core.logger import logger
from app.model.users import User, UserCollection
import pytest
import httpx



BASE_URL = "http://127.0.0.1:8000"
# Use httpx.AsyncClient for async requests
@pytest.mark.asyncio
async def test_list_users_service_existing_users():
    """Test list_users_service with real users already in the database."""
    result = await list_users_service()

    # Ensure the result is a UserCollection
    assert isinstance(result, UserCollection), "Result should be a UserCollection"
    assert len(result.users) > 0, "UserCollection should contain users"

    # Validate the first user (assuming at least one user exists)
    first_user = result.users[0]
    assert isinstance(first_user, User), "Each user should be a User model"
    assert hasattr(first_user, "username"), "User should have a username"
    assert hasattr(first_user, "email"), "User should have an email"
    assert hasattr(first_user, "xid"), "User should have an xid"

    print(f"✅ Retrieved {len(result.users)} users successfully!")

