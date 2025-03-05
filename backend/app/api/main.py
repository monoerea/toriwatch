
from fastapi import Body, HTTPException, status
from fastapi.responses import Response

from bson import ObjectId
from pymongo import ReturnDocument

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, RedirectResponse
from app.core.config import get_settings
from .models import User

settings = get_settings()

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION, summary=settings.SUMMARY)

@app.get("/", response_class=RedirectResponse)
async def home():
    return RedirectResponse(url=settings.API_PREFIX)

@app.get("/settings")
async def get_config():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
    }

@app.post(
    "/users/",
    response_description="Add new student",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_student(student: User = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_student = await student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = await student_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return created_student


@app.get(
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
    return StudentCollection(students=await student_collection.find().to_list(1000))


@app.get(
    "/students/{id}",
    response_description="Get a single student",
    response_model=User,
    response_model_by_alias=False,
)
async def show_student(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        student := await student_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put(
    "/students/{id}",
    response_description="Update a student",
    response_model=User,
    response_model_by_alias=False,
)
async def update_student(id: str, student: UpdateUser = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    student = {
        k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
    }

    if len(student) >= 1:
        update_result = await student_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": student},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_student := await student_collection.find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/students/{id}", response_description="Delete a student")
async def delete_student(id: str):
    """
    Remove a single student record from the database.
    """
    delete_result = await student_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")