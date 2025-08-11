from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: str
    priority: int
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int  # You can assign this dynamically later

    class Config:
        from_attributes = True

