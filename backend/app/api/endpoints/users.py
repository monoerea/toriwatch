from typing_extensions import Annotated
from fastapi import APIRouter
from pymongo import ReturnDocument
from pydantic import BeforeValidator
from fastapi import Body, HTTPException, status
from fastapi.responses import Response
from app.model.models import AccountClassification, User, UserCollection, UpdateUserModel, UpdateAccountClassification
from app.core.logger import logger
from app.core.db import user_collection

router = APIRouter()

ObjectId = Annotated[str, BeforeValidator(str)]

@router.get("/", response_description="Get all users", response_model=UserCollection, status_code=status.HTTP_200_OK,response_model_by_alias=False)
async def list_users():
    if user_collection is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    try:
        users_cursor = await user_collection.find().to_list(10)
        users = [User(id=str(user["_id"]), **user) for user in users_cursor]
        return UserCollection(users=users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.post("/", response_description="Add new user", response_model=User, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def create_user(user: User = Body(...)):
    # Check for duplicate users if needed
    if await user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    user_data = user.model_dump(by_alias=True, exclude={"id"})

    new_user = await user_collection.insert_one(user_data)

    created_user = await user_collection.find_one({"_id": new_user.inserted_id})

    if not created_user:
        raise HTTPException(status_code=500, detail="User creation failed")

    created_user_model = User(**created_user)

    return created_user_model

@router.get("/{id}", response_description="Get a single user", response_model=User, response_model_by_alias=False)
async def show_user(id: str):
    if user := await user_collection.find_one({"_id": ObjectId(id)}):
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.put("/{id}", response_description="Update a user", response_model=User, response_model_by_alias=False)
async def update_user(id: str, user: UpdateUserModel = Body(...), account_classification: UpdateAccountClassification = Body(...)):
    # Update user fields
    user_data = {k: v for k, v in user.model_dump(by_alias=True).items() if v is not None}

    if account_classification.label or account_classification.confidence_score:  # Check if account classification is updated
        user_data["account_classification"] = account_classification.model_dump(exclude_unset=True)

    if len(user_data) >= 1:
        update_result = await user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user_data},
            return_document=ReturnDocument.AFTER
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    # Return the existing user if no update was performed
    if existing_user := await user_collection.find_one({"_id": ObjectId(id)}):
        return existing_user
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete("/{id}", response_description="Delete a user")
async def delete_user(id: str):
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User {id} not found")
