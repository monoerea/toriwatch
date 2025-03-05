from fastapi import APIRouter
from .endpoints import users

api_router = APIRouter(prefix="/api")

api_router.include_router(users.router, prefix="/users")
