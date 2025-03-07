from fastapi import HTTPException, status
from app.repositories.user import get_user_by_id, create_user, update_user, delete_user, list_users
from app.model.users import User, UserUpdate, UpdateAccountClassification, UserCollection, UserCreate

async def list_users_service() -> UserCollection:
    """Fetch all users and return them as a UserCollection."""
    try:
        user_cursor = await list_users()
        if not user_cursor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

        user_objects = [
            User(**{**user, "_id": str(user["_id"])}) for user in user_cursor
        ]
        return UserCollection(users=user_objects)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def create_user_service(user: UserCreate) -> User:
    """Create a new user and return the User model with error handling."""
    try:
        user_data = user.model_dump(by_alias=True, exclude={"id"})
        new_user = await create_user(user_data)
        if not new_user:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")

        return User(**new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_user_service(user_id: str) -> User:
    """Fetch a user by ID with error handling."""
    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        return User(**user)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def update_user_service(user_id: str, user: UserUpdate, account_classification: UpdateAccountClassification) -> User:
    """Update a user with error handling."""
    try:
        update_data = {k: v for k, v in user.model_dump(by_alias=True).items() if v is not None}
        if account_classification.label or account_classification.confidence_score:
            update_data["account_classification"] = account_classification.model_dump(exclude_unset=True)

        updated_user = await update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found or update failed")

        return User(**updated_user)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_user_service(user_id: str) -> None:
    """Delete a user by ID with error handling."""
    try:
        deleted = await delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
