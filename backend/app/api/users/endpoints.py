from fastapi import APIRouter, status
from app.services.users import list_users_service, get_user_service, create_user_service, delete_user_service
from app.model.users import UserCollection, User, UserCreate

router = APIRouter()

@router.get("/", response_description="Get all users", response_model=UserCollection, status_code=status.HTTP_200_OK,response_model_by_alias=False)
async def list_users_endpoint():
    return await list_users_service()

@router.put("/{uid}", response_description="Get a user by id", response_model=User, status_code=status.HTTP_200_OK,response_model_by_alias=False)
async def get_user_by_id_endpoint(uid: str):
    return await get_user_by_id_service(user_id=uid)

@router.post("/", response_description="Create a user", response_model=UserCreate, status_code=status.HTTP_200_OK,response_model_by_alias=False)
async def create_user_endpoint(user: UserCreate):
    return await create_user_service(user_data=user)

@router.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    return await delete_user_service(id=id)
