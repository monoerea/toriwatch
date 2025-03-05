import os
from typing_extensions import Annotated
from fastapi import APIRouter
import motor
from model import User, UserCollection, UpdateUserModel
import motor.motor_asyncio
from pymongo import ReturnDocument
from pydantic import BeforeValidator
from pymongo import ReturnDocument
from fastapi import Body, HTTPException, status
from fastapi.responses import Response

router = APIRouter()

from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.college
user_collection = db.get_collection("users")
PyObjectId = Annotated[str, BeforeValidator(str)]


@router.get( "/users/",
    response_description="Get all users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,)

@router.post(
    "/users/",
    response_description="Add new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: User = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_student = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return created_user


@router.get(
    "/students/",
    response_description="List all students",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_students():
    """
    List all of the student data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return UserCollection(students=await user_collection.find().to_list(1000))


@router.get(
    "/users/{id}",
    response_description="Get a single student",
    response_model=User,
    response_model_by_alias=False,
)
async def show_student(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        user := await user_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.put(
    "/users/{id}",
    response_description="Update a student",
    response_model=User,
    response_model_by_alias=False,
)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    user = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }

    if len(user) >= 1:
        update_result = await user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := await user_collection.find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.delete("/users/{id}", response_description="Delete a student")
async def delete_user(id: str):
    """
    Remove a single student record from the database.
    """
    delete_result = await user_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")