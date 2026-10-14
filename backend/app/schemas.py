from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .models import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    tags: Optional[str] = None


class TaskResponse(TaskBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TaskStats(BaseModel):
    total: int
    todo: int
    in_progress: int
    review: int
    done: int
    high_priority: int
    critical_priority: int
