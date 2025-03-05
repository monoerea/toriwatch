
import os
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Literal
import motor.motor_asyncio
from pymongo import ReturnDocument
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
student_collection = db.get_collection("students")
PyObjectId = Annotated[str, BeforeValidator(str)]

class AccountClassification(BaseModel):
    label: Literal["bot", "human", "suspicious"]
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score from 0 to 1")

    @validator("confidence_score")
    def check_confidence(cls, value):
        if value < 0.5 and value > 0:
            raise ValueError("Confidence score is too low to classify the account reliably.")
        return value

class User(BaseModel):
    _id: int = Field(default=False, description="Id of the user's X account")
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

    @validator("username")
    def validate_username(cls, value):
        if not value.isalnum() and "_" not in value:
            raise ValueError("Username must contain only letters, numbers, or underscores.")
        return value

    @validator("engagement_score")
    def validate_engagement_score(cls, value):
        if value > 0.9:
            raise ValueError("Engagement score is too high, possible bot activity.")
        return value

    class Config:
        json_schema_extra = {
            "example": {
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