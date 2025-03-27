import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from unittest.mock import AsyncMock
from datetime import datetime
from httpx import AsyncClient
from fastapi.testclient import TestClient
from backend.main import app  # Ensure this is your FastAPI app instance
from app.dependencies.users import get_user_service
from app.model.users import User, UserCollection, AccountClassification, UserCreate
import secrets

BASE_URL = "http://test"

@pytest.fixture
def mock_user_service():
    """Mocked UserService dependency."""
    mock_service = AsyncMock()

    # Sample user data
    sample_user = User(
        id="60b8d6a4f1a4c2a5d8e9b917",
        xid=12345678,
        username="example_user",
        email="user@example.com",
        twitter_access_token=secrets.token_hex(16),
        twitter_access_token_secret=secrets.token_hex(16),
        has_access=True,
        is_authenticated=True,
        account_classification=AccountClassification(label="bot", confidence_score=0.85),
        created_at=datetime.now(),
        follower_count=1200,
        following_count=300,
        tweet_count=5000,
        engagement_score=0.75
    )

    mock_service.list_users.return_value = UserCollection(users=[sample_user])
    mock_service.get_user_by_id.return_value = sample_user
    mock_service.create_user.side_effect = lambda user_data: User(
        id="new_generated_id",
        xid=user_data.xid,
        username=user_data.username,
        email=user_data.email,
        twitter_access_token=secrets.token_hex(16),
        twitter_access_token_secret=secrets.token_hex(16),
        has_access=user_data.has_access,
        is_authenticated=user_data.is_authenticated,
        account_classification=AccountClassification(label="human", confidence_score=0.9),
        created_at=datetime.now(),
        follower_count=100,
        following_count=50,
        tweet_count=200,
        engagement_score=0.6
    )
    mock_service.delete_user.return_value = None  # No content for delete

    return mock_service

@pytest.fixture
async def client(mock_user_service):
    """Test client with mocked dependency."""
    app.dependency_overrides[get_user_service] = lambda: mock_user_service
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        yield ac
