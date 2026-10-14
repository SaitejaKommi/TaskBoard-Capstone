import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base

# In-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["application"] == "TaskBoard"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "READY"


def test_create_task():
    payload = {
        "title": "Test Task",
        "description": "A test task",
        "status": "todo",
        "priority": "high",
        "assignee": "alice",
        "due_date": "2026-12-31",
        "tags": "testing,backend",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert "id" in data


def test_list_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task():
    # Create first
    create_resp = client.post("/api/tasks", json={"title": "Get Me", "priority": "low"})
    task_id = create_resp.json()["id"]
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task():
    create_resp = client.post("/api/tasks", json={"title": "Old Title"})
    task_id = create_resp.json()["id"]
    response = client.put(f"/api/tasks/{task_id}", json={"title": "New Title", "status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["status"] == "in_progress"


def test_delete_task():
    create_resp = client.post("/api/tasks", json={"title": "Delete Me"})
    task_id = create_resp.json()["id"]
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204
    # Confirm deleted
    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_task_stats():
    response = client.get("/api/tasks/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "todo" in data
    assert "done" in data


def test_get_task_not_found():
    response = client.get("/api/tasks/99999")
    assert response.status_code == 404


def test_filter_tasks_by_status():
    client.post("/api/tasks", json={"title": "Filter Test", "status": "done"})
    response = client.get("/api/tasks?status=done")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["status"] == "done" for t in tasks)


def test_create_task_missing_title():
    response = client.post("/api/tasks", json={"priority": "high"})
    assert response.status_code == 422
