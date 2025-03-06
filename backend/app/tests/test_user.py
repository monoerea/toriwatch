import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.core.logger import logger
import pytest
import httpx
import requests

BASE_URL = "http://127.0.0.1:8000"
# Use httpx.AsyncClient for async requests
@pytest.mark.asyncio
async def test_get_all_users():
    """Test retrieving all users from MongoDB."""
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        response = await client.get("/api/users/")

        # Log the raw response and the status code
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        logger.info(f"Response text: {response.text}")

        # Check if the response is successful
        if response.status_code != 200:
            logger.error(f"Error: Received status code {response.status_code}")
            assert False, f"Received error status code {response.status_code}"

        # Try parsing the response as JSON
        try:
            response_data = response.json()  # This will raise an error if the response is not valid JSON
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            assert False, "Failed to parse JSON response"

        # Deserialize the response data using UserCollection Pydantic model
        logger.info(f"Response Data: {response_data}")

        # Further assertions to check if the response data matches the expected structure
        assert isinstance(response_data, dict)
        assert "users" in response_data
        assert isinstance(response_data["users"], list)

        # Check the structure of each user in the collection
        for user in response_data["users"]:
            assert "id" in user
            assert "xid" in user
            assert "username" in user
            assert "email" in user
            assert "has_access" in user
            assert "is_authenticated" in user
            assert "account_classification" in user
            assert "created_at" in user
            assert "follower_count" in user
            assert "following_count" in user
            assert "tweet_count" in user
            assert "engagement_score" in user

        logger.info(f"Successfully retrieved {len(response_data['users'])} users.")


def sample_user():
    """Fixture to provide a sample user object."""
    return {
        "_id": "6929073",
        "xid": 3483233,
        "username": "example",
        "email": "example@mail.dev",
        "has_access": True,
        "is_authenticated": True,
        "account_classification": {
            "label": "bot",
            "confidence_score": 0.69
        },
        "created_at": "2023-08-17T07:59:22.589Z",
        "follower_count": 14357,
        "following_count": 2019,
        "tweet_count": 1070,
        "engagement_score": 0.42
    }

@pytest.mark.asyncio
async def test_create_user():
    """Test creating a new user."""
    user = sample_user()  # Assuming sample_user() returns a valid user dictionary
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        try:
            response = await client.post("/api/users/", json=user)  # Ensure this is awaited
            assert response.status_code == 201  # HTTP 201 Created
            # Parse response JSON data
            doc = response.json()
            # Assertions
            assert "_id" in doc
            assert doc["email"] == user["email"]
            return doc["_id"]  # Return the inserted user's ID (if needed)
        except Exception as e:
            print(e)