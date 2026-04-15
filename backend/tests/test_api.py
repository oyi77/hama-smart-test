import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_todo():
    response = client.post(
        "/api/todos/",
        json={"title": "Test Todo", "description": "Test Description", "category": "Work"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["category"] == "Work"
    assert "id" in data

def test_read_todos():
    client.post("/api/todos/", json={"title": "Todo 1"})
    client.post("/api/todos/", json={"title": "Todo 2"})
    
    response = client.get("/api/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_todo():
    create_res = client.post("/api/todos/", json={"title": "Old Title"})
    todo_id = create_res.json()["id"]
    
    response = client.put(f"/api/todos/{todo_id}", json={"title": "New Title", "is_done": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["is_done"] is True

def test_delete_todo():
    create_res = client.post("/api/todos/", json={"title": "To Delete"})
    todo_id = create_res.json()["id"]
    
    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    
    get_res = client.get(f"/api/todos/{todo_id}")
    assert get_res.status_code == 404
