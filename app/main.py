from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from datetime import timedelta
from typing import List
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.models import TaskCreate, TaskUpdate, TaskResponse
from app.user_models import UserCreate, UserLogin, TokenResponse, UserResponse
from app.config import settings
from app.security import SecurityUtils
from app.auth import get_current_user
from app.exceptions import UnauthorizedException, ConflictException, NotFoundException
from app.logger import logger
from app import crud, user_crud

app = FastAPI(
    title="Task API",
    description="A Task Management API with JWT Authentication built with FastAPI and MongoDB",
    version="2.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    logger.info("Database connection established")

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    logger.info("Database connection closed")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Task API v2.0"}

@app.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register(user: UserCreate, db=Depends(get_database)):
    logger.info(f"Registration attempt for email: {user.email}")
    created_user = await user_crud.create_user(db, user)
    if not created_user:
        logger.warning(f"Registration failed - email already exists: {user.email}")
        raise ConflictException("Email already registered")
    logger.info(f"User registered successfully: {user.email}")
    
    access_token_expires = timedelta(hours=settings.access_token_expire_hours)
    access_token = SecurityUtils.create_access_token(
        data={"sub": created_user.email}, expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        user=created_user
    )

@app.post("/auth/login", response_model=TokenResponse, tags=["Authentication"])
async def login(user_login: UserLogin, db=Depends(get_database)):
    logger.info(f"Login attempt for email: {user_login.email}")
    user = await user_crud.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        logger.warning(f"Login failed for email: {user_login.email}")
        raise UnauthorizedException("Invalid email or password")
    
    access_token_expires = timedelta(hours=settings.access_token_expire_hours)
    access_token = SecurityUtils.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in successfully: {user_login.email}")
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=str(user["_id"]),
            email=user["email"],
            username=user["username"],
            created_at=user["created_at"]
        )
    )

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    logger.info(f"Creating task for user: {current_user['email']}")
    return await crud.create_task(db, task, str(current_user["_id"]))

@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    logger.info(f"Listing tasks for user: {current_user['email']}")
    return await crud.get_tasks(db, str(current_user["_id"]), skip, limit)

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(task_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    logger.info(f"Getting task {task_id} for user: {current_user['email']}")
    task = await crud.get_task(db, task_id, str(current_user["_id"]))
    if not task:
        logger.warning(f"Task not found: {task_id}")
        raise NotFoundException("Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    logger.info(f"Updating task {task_id} for user: {current_user['email']}")
    task = await crud.update_task(db, task_id, task_update, str(current_user["_id"]))
    if not task:
        logger.warning(f"Task not found or unauthorized: {task_id}")
        raise NotFoundException("Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_database)):
    logger.info(f"Deleting task {task_id} for user: {current_user['email']}")
    deleted = await crud.delete_task(db, task_id, str(current_user["_id"]))
    if not deleted:
        logger.warning(f"Task not found or unauthorized: {task_id}")
        raise NotFoundException("Task not found")
