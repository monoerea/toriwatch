from fastapi import APIRouter
from .users.endpoints import router as user_router
from .tweets.endpoints import router as tweets_router
api_router = APIRouter(prefix="/api")

api_router.include_router(user_router, prefix="/users")
api_router.include_router(tweets_router, prefix="/tweets")
