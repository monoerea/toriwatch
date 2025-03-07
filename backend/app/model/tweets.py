


from typing import List
from pydantic import BaseModel, Field

class Tweet(BaseModel):
    username: str = Field(..., min_length=4, max_length=50, pattern = r'^[\w\.-]+$', description="User's username")
class TweetCollection (BaseModel):
    tweets: List[Tweet]