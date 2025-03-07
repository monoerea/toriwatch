from fastapi import Depends
from app.core.db import user_collection

def get_user_collection():
    return user_collection