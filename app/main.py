# # from fastapi import FastAPI

# # app = FastAPI()

# # @app.get("/")
# # def read_root():
# #     return {"message": "Hello, Dynamic Task Allocator!"}

# # main.py





# #111111111111111111111111111111111111111






# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from typing import Optional, List, Dict
# from uuid import uuid4
# from datetime import datetime

# app = FastAPI(
#     title="Dynamic Task Allocator & Load Balancer",
#     version="0.1",
#     description="Step 2: Basic routes + placeholders (in-memory)."
# )

# # ---------- Pydantic models (request/response shapes) ----------
# class TaskCreate(BaseModel):
#     title: str = Field(..., example="Process user data")
#     priority: int = Field(..., ge=0, example=5)  # higher = more urgent (we'll define convention later)
#     estimated_duration: int = Field(..., ge=0, example=10)  # seconds, for simulation
#     metadata: Optional[Dict] = Field(default=None, example={"type":"batch","owner":"team-a"})

# class Task(TaskCreate):
#     id: str
#     status: str
#     submitted_at: datetime
#     assigned_to: Optional[str] = None
#     assigned_at: Optional[datetime] = None

# class WorkerCreate(BaseModel):
#     node_id: str = Field(..., example="worker-1")
#     capacity: Optional[int] = Field(10, example=10)  # abstract capacity units

# class Worker(BaseModel):
#     node_id: str
#     capacity: int
#     current_load: int = 0
#     registered_at: datetime

# # ---------- In-memory stores (temporary; later replace with DB) ----------
# _tasks: Dict[str, Task] = {}          # task_id -> Task
# _workers: Dict[str, Worker] = {}      # node_id -> Worker

# # ---------- Health endpoint ----------
# @app.get("/ping")
# def ping():
#     return {"status": "ok", "now": datetime.utcnow().isoformat()}

# # ---------- Task endpoints ----------
# @app.post("/tasks", response_model=Task, status_code=201)
# def create_task(payload: TaskCreate):
#     task_id = str(uuid4())
#     now = datetime.utcnow()
#     task = Task(
#         id=task_id,
#         title=payload.title,
#         priority=payload.priority,
#         estimated_duration=payload.estimated_duration,
#         metadata=payload.metadata,
#         status="pending",
#         submitted_at=now,
#     )
#     _tasks[task_id] = task
#     return task

# @app.get("/tasks", response_model=List[Task])
# def list_tasks():
#     # return as list, sorted by submitted_at desc (simple)
#     return sorted(list(_tasks.values()), key=lambda t: t.submitted_at)

# @app.get("/tasks/{task_id}", response_model=Task)
# def get_task(task_id: str):
#     task = _tasks.get(task_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return task

# # Manual assignment placeholder (we will automate later)
# @app.post("/tasks/{task_id}/assign")
# def assign_task(task_id: str, worker_id: str):
#     task = _tasks.get(task_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     worker = _workers.get(worker_id)
#     if not worker:
#         raise HTTPException(status_code=404, detail="Worker not found")
#     if task.status != "pending":
#         raise HTTPException(status_code=400, detail=f"Task status is {task.status}, cannot assign")
#     # simple assignment placeholder: mark assigned, increment load
#     task.assigned_to = worker.node_id
#     task.assigned_at = datetime.utcnow()
#     task.status = "assigned"
#     worker.current_load += task.estimated_duration
#     _workers[worker.node_id] = worker
#     _tasks[task_id] = task
#     return {"message": "assigned", "task_id": task_id, "worker_id": worker.node_id}

# # ---------- Worker endpoints ----------
# @app.post("/workers", response_model=Worker, status_code=201)
# def register_worker(payload: WorkerCreate):
#     if payload.node_id in _workers:
#         raise HTTPException(status_code=400, detail="Worker already registered")
#     now = datetime.utcnow()
#     w = Worker(node_id=payload.node_id, capacity=payload.capacity, current_load=0, registered_at=now)
#     _workers[payload.node_id] = w
#     return w

# @app.get("/workers", response_model=List[Worker])
# def list_workers():
#     return list(_workers.values())


from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Dynamic Task Allocator & Load Balancer"}
