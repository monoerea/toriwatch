from typing import Optional, List, Literal
from fastapi import Depends
from typing_extensions import Annotated
from pydantic import BaseModel, Field, EmailStr, SecretStr, field_validator, ConfigDict
from datetime import datetime
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from backend.main import app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AccountClassification(BaseModel):
    label: Literal["bot", "human", "suspicious"]
    confidence_score: float = Field(..., ge=0.5, le=1.0, description="Confidence score from 0.5 to 1.0")

    @field_validator("confidence_score")
    @classmethod
    def check_confidence(cls, value):
        if value < 0.5:
            raise ValueError("Confidence score must be at least 0.5 for reliable classification.")
        return value

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
class User(BaseModel):
    id: str = Field(..., description="My generated id")
    xid: int = Field(..., description="ID of the user's X account")
    username: str = Field(..., min_length=4, max_length=50, pattern=r'^[\w\.-]+$', description="User's username")
    created_at: datetime = Field(..., description="Twitter account creation date")
    twitter_access_token: SecretStr
    twitter_access_token_secret: SecretStr

    account_classification: Optional[AccountClassification] = Field(None, description="Classification of the user's account")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    follower_count: Optional[int] = Field(None, ge=0, description="Number of followers")
    following_count: Optional[int] = Field(None, ge=0, description="Number of accounts the user is following")
    tweet_count: Optional[int] = Field(None, ge=0, description="Number of tweets by the user")
    
    has_access: bool = Field(..., description="User has access to the bot")
    is_authenticated: bool = Field(..., description="User authenticated with Twitter")

    engagement_score: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="Engagement score from 0-1")

    @field_validator("engagement_score")
    @classmethod
    def validate_engagement_score(cls, value):
        if value > 1:
            raise ValueError("Engagement score is too high, possible bot activity.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "6929073",
                "xid": "3435342",
                "username": "example_user",
                "email": "user@example.com",
                "has_access": True,
                "is_authenticated": True,
                "account_classification": None,  # Initially None
                "created_at": "2023-06-12T15:23:00",
                "follower_count": 1200,
                "following_count": 300,
                "tweet_count": 5000,
                "engagement_score": 0.75
            }
        }
    )


class UpdateAccountClassification(BaseModel):
    label: Optional[Literal["bot", "human", "suspicious"]] = None
    confidence_score: Optional[float] = Field(None, ge=0.5, le=1.0, description="Updated confidence score")


class UpdateUserModel(BaseModel):
    """
    A set of optional updates to be made to a user document in the database.
    """
    xid: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    has_access: Optional[bool] = None
    is_authenticated: Optional[bool] = None
    account_classification: Optional[UpdateAccountClassification] = None
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    tweet_count: Optional[int] = None
    engagement_score: Optional[float] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "updated_user",
                "email": "updated_email@example.com",
                "has_access": True,
                "is_authenticated": True,
                "account_classification": {
                    "label": "human",
                    "confidence_score": 0.85
                },
                "follower_count": 1300,
                "following_count": 350,
                "tweet_count": 5200,
                "engagement_score": 0.68
            }
        }
    )

class UserCollection(BaseModel):
    """
    A container holding a list of `User` instances.

    This avoids vulnerabilities related to returning top-level JSON arrays.
    """
    users: List[User]
