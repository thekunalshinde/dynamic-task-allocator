from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.task import TaskCreate, Task  # We'll create these schemas soon

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# In-memory tasks store (for now)
tasks_db = []

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate):
    # For now, just append to in-memory list
    tasks_db.append(task)
    return task

@router.get("/", response_model=List[Task])
async def list_tasks():
    return tasks_db
