from typing_extensions import Annotated
from fastapi import APIRouter, Depends, status
from app.model.tweets import TweetCollection
from app.core.db import db
from fastapi import HTTPException, Query
from typing import List, Optional

router = APIRouter()

@router.get("/", response_description="Get all tweets", response_model=TweetCollection, status_code=status.HTTP_200_OK,response_model_by_alias=False)
async def get_tweets_endpoint(args):
    """_summary_

    Args:
        args (_type_): _description_
    """
    pass
