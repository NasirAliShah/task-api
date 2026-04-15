from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models import TaskCreate, TaskUpdate, TaskResponse

async def create_task(db: AsyncIOMotorDatabase, task: TaskCreate) -> TaskResponse:
    task_dict = task.model_dump()
    task_dict["created_at"] = datetime.utcnow()
    task_dict["updated_at"] = datetime.utcnow()
    
    result = await db.tasks.insert_one(task_dict)
    created_task = await db.tasks.find_one({"_id": result.inserted_id})
    
    return TaskResponse(
        id=str(created_task["_id"]),
        title=created_task["title"],
        description=created_task.get("description"),
        completed=created_task["completed"],
        created_at=created_task["created_at"],
        updated_at=created_task["updated_at"]
    )

async def get_tasks(db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 100) -> List[TaskResponse]:
    tasks = []
    cursor = db.tasks.find().skip(skip).limit(limit).sort("created_at", -1)
    
    async for task in cursor:
        tasks.append(TaskResponse(
            id=str(task["_id"]),
            title=task["title"],
            description=task.get("description"),
            completed=task["completed"],
            created_at=task["created_at"],
            updated_at=task["updated_at"]
        ))
    
    return tasks

async def get_task(db: AsyncIOMotorDatabase, task_id: str) -> Optional[TaskResponse]:
    if not ObjectId.is_valid(task_id):
        return None
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    
    if task:
        return TaskResponse(
            id=str(task["_id"]),
            title=task["title"],
            description=task.get("description"),
            completed=task["completed"],
            created_at=task["created_at"],
            updated_at=task["updated_at"]
        )
    
    return None

async def update_task(db: AsyncIOMotorDatabase, task_id: str, task_update: TaskUpdate) -> Optional[TaskResponse]:
    if not ObjectId.is_valid(task_id):
        return None
    
    update_data = {k: v for k, v in task_update.model_dump(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        return await get_task(db, task_id)
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        return None
    
    return await get_task(db, task_id)

async def delete_task(db: AsyncIOMotorDatabase, task_id: str) -> bool:
    if not ObjectId.is_valid(task_id):
        return False
    
    result = await db.tasks.delete_one({"_id": ObjectId(task_id)})
    
    return result.deleted_count > 0
