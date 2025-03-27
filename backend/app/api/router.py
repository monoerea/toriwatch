from fastapi import APIRouter
from backend.app.api.endpoints.users import router as user_router
from  backend.app.api.endpoints.tweets import router as tweets_router

api_router = APIRouter(prefix="/api")

api_router.include_router(user_router, prefix="/users")
api_router.include_router(tweets_router, prefix="/tweets")
