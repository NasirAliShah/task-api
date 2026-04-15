from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.models import TaskCreate, TaskUpdate, TaskResponse
from app import crud

app = FastAPI(
    title="Task API",
    description="A simple Task Management API built with FastAPI and MongoDB",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Task API"}

@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate, db=Depends(get_database)):
    return await crud.create_task(db, task)

@app.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
async def list_tasks(skip: int = 0, limit: int = 100, db=Depends(get_database)):
    return await crud.get_tasks(db, skip, limit)

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def get_task(task_id: str, db=Depends(get_database)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_task(task_id: str, task_update: TaskUpdate, db=Depends(get_database)):
    task = await crud.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: str, db=Depends(get_database)):
    deleted = await crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
