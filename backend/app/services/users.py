from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.model.users import User, UserUpdate, UpdateAccountClassification, UserCollection
from motor.motor_asyncio import AsyncIOMotorDatabase

class UserService:
    def __init__(self, db:AsyncIOMotorDatabase):
        self.repository = UserRepository(db)

    async def list_users(self) -> UserCollection:
        """Fetch all users and return them as a UserCollection."""
        try:
            user_cursor = await self.repository.list_users()
            if not user_cursor:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

            user_objects = [
                User(**{**user, "_id": str(user["_id"])}) for user in user_cursor
            ]
            return UserCollection(users=user_objects)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def create_user(self, user_data: dict) -> User:
        """Create a new user and return the User model with error handling."""
        try:
            new_user = await self.repository.create_user(user_data)
            if not new_user:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")

            return User(**new_user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user(self, user_id: str) -> User:
        """Fetch a user by ID with error handling."""
        try:
            user = await self.repository.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
            return User(**user)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def update_user(self, user_id: str, user: UserUpdate, account_classification: UpdateAccountClassification) -> User:
        """Update a user with error handling."""
        try:
            # update_data = {k: v for k, v in user.model_dump(by_alias=True, exclude_unset=True).items() if v is not None}
            # if account_classification.label or account_classification.confidence_score:
            #     update_data["account_classification"] = account_classification.model_dump(exclude_unset=True)
            update_data = user.model_dump(by_alias=True, exclude_unset=True)
            updated_user = await self.repository.update_user(user_id, update_data)
            if not updated_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found or update failed")

            return User(**updated_user)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def delete_user(self, user_id: str) -> None:
        """Delete a user by ID with error handling."""
        try:
            deleted = await self.repository.delete_user(user_id)
            if not deleted:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error in deleting {user_id}: {str(e)}"
            )