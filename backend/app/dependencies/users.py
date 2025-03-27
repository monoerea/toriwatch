from app.repositories.user import UserRepository
from app.services.users import UserService

def get_user_service():
    user_repository = UserRepository()  # Initialize repository
    return UserService(user_repository)
