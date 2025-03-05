from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Users"])
async def get_users():
    return {"message": "List of users"}
