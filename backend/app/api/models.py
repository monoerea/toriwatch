from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_settings import ConfigDict
from datetime import datetime
from bson import ObjectId

class AccountClassification(BaseModel):
    label: Literal["bot", "human", "suspicious"]
    confidence_score: float = Field(..., ge=0.5, le=1.0, description="Confidence score from 0.5 to 1.0")

    @field_validator("confidence_score")
    @classmethod
    def check_confidence(cls, value):
        if value < 0.5:
            raise ValueError("Confidence score must be at least 0.5 for reliable classification.")
        return value


class User(BaseModel):
    _id: int = Field(..., description="ID of the user's X account")
    username: str = Field(..., min_length=4, max_length=50, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr
    has_access: bool = Field(default=False, description="User has access to the bot")
    is_authenticated: bool = Field(default=False, description="User authenticated with Twitter")
    account_classification: AccountClassification
    created_at: datetime = Field(..., description="Twitter account creation date")
    follower_count: int = Field(..., ge=0)
    following_count: int = Field(..., ge=0)
    tweet_count: int = Field(..., ge=0)
    engagement_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Engagement score from 0-1")

    @field_validator("engagement_score")
    @classmethod
    def validate_engagement_score(cls, value):
        if value > 0.9:
            raise ValueError("Engagement score is too high, possible bot activity.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "_id": 6929073,
                "username": "example_user",
                "email": "user@example.com",
                "has_access": True,
                "is_authenticated": True,
                "account_classification": {
                    "label": "bot",
                    "confidence_score": 0.92
                },
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
