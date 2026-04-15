from datetime import datetime
from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.user_models import UserCreate, UserLogin, UserResponse
from app.security import SecurityUtils

async def create_user(db: AsyncIOMotorDatabase, user: UserCreate) -> UserResponse:
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        return None
    
    user_dict = {
        "email": user.email,
        "username": user.username,
        "hashed_password": SecurityUtils.hash_password(user.password),
        "created_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return UserResponse(
        id=str(created_user["_id"]),
        email=created_user["email"],
        username=created_user["username"],
        created_at=created_user["created_at"]
    )

async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[dict]:
    return await db.users.find_one({"email": email})

async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> Optional[UserResponse]:
    if not ObjectId.is_valid(user_id):
        return None
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if user:
        return UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            username=user["username"],
            created_at=user["created_at"]
        )
    
    return None

async def authenticate_user(db: AsyncIOMotorDatabase, email: str, password: str) -> Optional[dict]:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    
    if not SecurityUtils.verify_password(password, user["hashed_password"]):
        return None
    
    return user
