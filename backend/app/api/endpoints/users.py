from fastapi import APIRouter, Depends, status
from app.services.users import UserService
from app.model.users import UserCollection, User, UserCreate
from app.dependencies.users import get_user_service
router = APIRouter()

@router.get("/", response_description="Get all users", response_model=UserCollection, status_code=status.HTTP_200_OK)
async def list_users_endpoint(user_service: UserService = Depends(get_user_service)):
    return await user_service.list_users()

@router.get("/{uid}", response_description="Get a user by id", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id_endpoint(uid: str, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user_by_id(user_id=uid)

@router.post("/", response_description="Create a user", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(user_data=user)

@router.delete("/{uid}", response_description="Delete a user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(uid: str, user_service: UserService = Depends(get_user_service)):
    return await user_service.delete_user(user_id=uid)