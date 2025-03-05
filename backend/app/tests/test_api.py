import pytest
import requests

# Base URL for the FastAPI backend
BASE_URL = "http://localhost:8000/users/"

@pytest.fixture
def sample_user():
    """Fixture to provide a sample user object."""
    return {
        "_id": 6929073,
        "username": "Krzysztof_Su3",
        "email": "josefa+van-der-linden815@mail.dev",
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

def test_create_user(sample_user):
    """Test creating a new user."""
    response = requests.post(BASE_URL, json=sample_user)
    assert response.status_code == 201  # HTTP 201 Created
    doc = response.json()
    assert "_id" in doc
    assert doc["email"] == sample_user["email"]
    return doc["_id"]  # Return the inserted user's ID

def test_get_users():
    """Test retrieving a list of users."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    users = response.json()["users"]
    assert isinstance(users, list)

def test_get_user_by_id():
    """Test retrieving a user by ID."""
    user_id = test_create_user(sample_user())  # Create user first
    response = requests.get(f"{BASE_URL}{user_id}")
    assert response.status_code == 200
    user = response.json()
    assert user["_id"] == user_id
    assert user["username"] == "Krzysztof_Su3"

def test_update_user():
    """Test updating an existing user."""
    user_id = test_create_user(sample_user())  # Create user first
    update_payload = {"email": "updated_email@example.com"}

    response = requests.put(f"{BASE_URL}{user_id}", json=update_payload)
    assert response.status_code == 200
    updated_user = response.json()

    assert updated_user["_id"] == user_id
    assert updated_user["email"] == "updated_email@example.com"

def test_delete_user():
    """Test deleting a user."""
    user_id = test_create_user(sample_user())  # Create user first
    response = requests.delete(f"{BASE_URL}{user_id}")
    assert response.status_code == 204  # No Content

    # Ensure user is deleted
    response = requests.get(f"{BASE_URL}{user_id}")
    assert response.status_code == 404  # Not Found
