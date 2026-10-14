from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import time
import os
from prometheus_fastapi_instrumentator import Instrumentator

from .database import engine, get_db, Base
from . import models, schemas

START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables as a fallback if Alembic migrations haven't been run."""
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception:
        pass  # DB may not be available during tests
    yield


app = FastAPI(
    title="TaskBoard API",
    description="A SaaS-style project management API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():
    return {
        "application": "TaskBoard",
        "version": "1.0.0",
        "status": "running",
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


@app.get("/health")
def health():
    return {"status": "healthy", "service": "taskboard-backend"}


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "READY", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database not ready: {str(e)}")


# ── Tasks ──────────────────────────────────────────────────────────────────────

@app.get("/api/tasks/stats", response_model=schemas.TaskStats)
def get_task_stats(db: Session = Depends(get_db)):
    total = db.query(models.Task).count()
    todo = db.query(models.Task).filter(models.Task.status == models.TaskStatus.todo).count()
    in_progress = db.query(models.Task).filter(models.Task.status == models.TaskStatus.in_progress).count()
    review = db.query(models.Task).filter(models.Task.status == models.TaskStatus.review).count()
    done = db.query(models.Task).filter(models.Task.status == models.TaskStatus.done).count()
    high_priority = db.query(models.Task).filter(models.Task.priority == models.TaskPriority.high).count()
    critical = db.query(models.Task).filter(models.Task.priority == models.TaskPriority.critical).count()
    return schemas.TaskStats(
        total=total, todo=todo, in_progress=in_progress,
        review=review, done=done,
        high_priority=high_priority, critical_priority=critical
    )


@app.get("/api/tasks", response_model=List[schemas.TaskResponse])
def list_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    assignee: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if assignee:
        query = query.filter(models.Task.assignee == assignee)
    return query.order_by(models.Task.created_at.desc()).all()


@app.get("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**task_in.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.put("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_in.model_dump(exclude_unset=True)
    for key, val in update_data.items():
        setattr(task, key, val)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
