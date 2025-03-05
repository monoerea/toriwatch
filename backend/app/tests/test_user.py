import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.core.logger import logger
import pytest
import httpx

# Use httpx.AsyncClient for async requests
@pytest.mark.asyncio
async def test_get_all_users():
    """Test retrieving all users from MongoDB."""
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000", timeout=30.0) as client:  # Set timeout to 30 seconds
        # Send GET request to the /api/users/ endpoint
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
