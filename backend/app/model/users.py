from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr, SecretStr, field_validator, ConfigDict
from datetime import datetime
from bson import ObjectId

# Field descriptions for documentation
ID_DESCRIPTION = "User's unique ID in MongoDB"
XID_DESCRIPTION = "User's X (Twitter) account ID"
USERNAME_DESCRIPTION = "User's username (must be alphanumeric with optional dots/hyphens)"
EMAIL_DESCRIPTION = "User's email address"
ACCESS_DESCRIPTION = "Whether the user has access to the bot"
AUTH_DESCRIPTION = "Whether the user is authenticated with Twitter"
TOKEN_DESCRIPTION = "User's Twitter access token (masked for security)"
TOKEN_SECRET_DESCRIPTION = "User's Twitter access token secret (masked for security)"
CLASSIFICATION_DESCRIPTION = "User's account classification based on bot detection"
CREATED_AT_DESCRIPTION = "Timestamp when the user was created"
FOLLOWER_COUNT_DESCRIPTION = "Total number of followers"
FOLLOWING_COUNT_DESCRIPTION = "Total number of users the user follows"
TWEET_COUNT_DESCRIPTION = "Total number of tweets made by the user"
ENGAGEMENT_SCORE_DESCRIPTION = "User's engagement score (0.0 - 1.0)"

from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class ObjectIdStr(str):
    """Pydantic-compatible representation of MongoDB ObjectId"""

    @classmethod
    def __get_pydantic_core_schema__(cls, handler: GetCoreSchemaHandler):
        """Define the Pydantic schema for ObjectIdStr"""
        return core_schema.str_schema()

    @classmethod
    def validate(cls, value):
        """Ensure the value is a valid ObjectId"""
        if isinstance(value, ObjectId):
            return str(value)
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return str(value)


class AccountClassification(BaseModel):
    label: Literal["bot", "human", "suspicious"] = Field(..., description="Classification label")
    confidence_score: float = Field(..., ge=0.5, le=1.0, description="Confidence score (0.5 - 1.0)")

    @field_validator("confidence_score")
    @classmethod
    def check_confidence(cls, value):
        if value < 0.5:
            raise ValueError("Confidence score must be at least 0.5")
        return value


class UserBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=50, pattern=r'^[\w\.-]+$', description=USERNAME_DESCRIPTION)


class UserCreate(UserBase):
    xid: int = Field(..., description=XID_DESCRIPTION)
    email: EmailStr = Field(..., description=EMAIL_DESCRIPTION)
    password: str = Field(..., min_length=4, max_length=50, description="User's password")
    twitter_access_token: SecretStr = Field(..., description=TOKEN_DESCRIPTION)
    twitter_access_token_secret: SecretStr = Field(..., description=TOKEN_SECRET_DESCRIPTION)
    has_access: bool = Field(..., description=ACCESS_DESCRIPTION)
    is_authenticated: bool = Field(..., description=AUTH_DESCRIPTION)


class UserUpdate(BaseModel):
    xid: Optional[int] = Field(None, description=XID_DESCRIPTION)
    username: Optional[str] = Field(None, min_length=4, max_length=50, pattern=r'^[\w\.-]+$', description=USERNAME_DESCRIPTION)
    email: Optional[EmailStr] = Field(None, description=EMAIL_DESCRIPTION)
    has_access: Optional[bool] = Field(None, description=ACCESS_DESCRIPTION)
    is_authenticated: Optional[bool] = Field(None, description=AUTH_DESCRIPTION)
    account_classification: Optional[AccountClassification] = Field(None, description=CLASSIFICATION_DESCRIPTION)
    follower_count: Optional[int] = Field(None, ge=0, description=FOLLOWER_COUNT_DESCRIPTION)
    following_count: Optional[int] = Field(None, ge=0, description=FOLLOWING_COUNT_DESCRIPTION)
    tweet_count: Optional[int] = Field(None, ge=0, description=TWEET_COUNT_DESCRIPTION)
    engagement_score: Optional[float] = Field(None, ge=0.0, le=1.0, description=ENGAGEMENT_SCORE_DESCRIPTION)


class User(UserBase):
    id: str = Field(..., alias="_id", description=ID_DESCRIPTION)
    xid: int = Field(..., description=XID_DESCRIPTION)
    email: Optional[str] = Field(None, description="User's email address")
    created_at: datetime = Field(..., description=CREATED_AT_DESCRIPTION)
    twitter_access_token: SecretStr = Field(..., description=TOKEN_DESCRIPTION)
    twitter_access_token_secret: SecretStr = Field(..., description=TOKEN_SECRET_DESCRIPTION)
    account_classification: Optional[AccountClassification] = Field(None, description=CLASSIFICATION_DESCRIPTION)
    follower_count: Optional[int] = Field(None, ge=0, description=FOLLOWER_COUNT_DESCRIPTION)
    following_count: Optional[int] = Field(None, ge=0, description=FOLLOWING_COUNT_DESCRIPTION)
    tweet_count: Optional[int] = Field(None, ge=0, description=TWEET_COUNT_DESCRIPTION)
    has_access: bool = Field(..., description=ACCESS_DESCRIPTION)
    is_authenticated: bool = Field(..., description=AUTH_DESCRIPTION)
    engagement_score: Optional[float] = Field(0.0, ge=0.0, le=1.0, description=ENGAGEMENT_SCORE_DESCRIPTION)

    @field_validator("engagement_score")
    @classmethod
    def validate_engagement_score(cls, value):
        if value > 1:
            raise ValueError("Engagement score cannot be greater than 1.0")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "60b8d6a4f1a4c2a5d8e9b917",
                "xid": 12345678,
                "username": "example_user",
                "email": "user@example.com",
                "twitter_access_token": "********",
                "twitter_access_token_secret": "********",
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


class UserCollection(BaseModel):
    users: List[User] = Field(..., description="List of users")
