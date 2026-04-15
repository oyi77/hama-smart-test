"""
Tests for todo API endpoints.
Follows Single Responsibility Principle - only tests todo API.
"""
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


def test_create_todo(client):
    """Test creating a todo via API."""
    # First create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Work", "color": "#FF5733"}
    )
    category_id = category_response.json()["id"]

    response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Complete project",
            "description": "Finish the implementation",
            "priority": "high",
            "category_id": category_id
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Complete project"
    assert data["completed"] is False
    assert data["priority"] == "high"


def test_get_todos(client):
    """Test getting all todos via API."""
    # Create a category first
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Personal", "color": "#3498DB"}
    )
    category_id = category_response.json()["id"]

    # Create some todos
    client.post(
        "/api/v1/todos/",
        json={"title": "First task", "priority": "low", "category_id": category_id}
    )
    client.post(
        "/api/v1/todos/",
        json={"title": "Second task", "priority": "medium", "category_id": category_id}
    )

    response = client.get("/api/v1/todos/")

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 2


def test_get_todo(client):
    """Test getting a specific todo via API."""
    # Create a category and todo
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Shopping", "color": "#2ECC71"}
    )
    category_id = category_response.json()["id"]

    todo_response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Buy groceries",
            "priority": "medium",
            "category_id": category_id
        }
    )
    todo_id = todo_response.json()["id"]

    response = client.get(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Buy groceries"


def test_update_todo(client):
    """Test updating a todo via API."""
    # Create a category and todo
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Work", "color": "#FF5733"}
    )
    category_id = category_response.json()["id"]

    todo_response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Original title",
            "priority": "medium",
            "category_id": category_id
        }
    )
    todo_id = todo_response.json()["id"]

    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={
            "title": "Updated title",
            "completed": True,
            "priority": "urgent"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["completed"] is True
    assert data["priority"] == "urgent"


def test_delete_todo(client):
    """Test deleting a todo via API."""
    # Create a category and todo
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Test", "color": "#FF0000"}
    )
    category_id = category_response.json()["id"]

    todo_response = client.post(
        "/api/v1/todos/",
        json={
            "title": "To delete",
            "priority": "low",
            "category_id": category_id
        }
    )
    todo_id = todo_response.json()["id"]

    response = client.delete(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404


def test_filter_todos_by_completed(client):
    """Test filtering todos by completion status."""
    # Create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Work", "color": "#FF5733"}
    )
    category_id = category_response.json()["id"]

    # Create completed and pending todos
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Completed task",
            "priority": "low",
            "completed": True,
            "category_id": category_id
        }
    )
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Pending task",
            "priority": "medium",
            "completed": False,
            "category_id": category_id
        }
    )

    # Get completed todos
    completed_response = client.get("/api/v1/todos/?completed=true")
    assert completed_response.status_code == 200
    completed_data = completed_response.json()
    assert len(completed_data["items"]) == 1

    # Get pending todos
    pending_response = client.get("/api/v1/todos/?completed=false")
    assert pending_response.status_code == 200
    pending_data = pending_response.json()
    assert len(pending_data["items"]) == 1


def test_filter_todos_by_priority(client):
    """Test filtering todos by priority."""
    # Create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Work", "color": "#FF5733"}
    )
    category_id = category_response.json()["id"]

    # Create todos with different priorities
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Low priority task",
            "priority": "low",
            "category_id": category_id
        }
    )
    client.post(
        "/api/v1/todos/",
        json={
            "title": "High priority task",
            "priority": "high",
            "category_id": category_id
        }
    )

    # Filter by high priority
    response = client.get("/api/v1/todos/?priority=high")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["priority"] == "high"


def test_search_todos(client):
    """Test searching todos via API."""
    # Create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Shopping", "color": "#2ECC71"}
    )
    category_id = category_response.json()["id"]

    # Create todos
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "priority": "medium",
            "category_id": category_id
        }
    )
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Complete homework",
            "description": "Math assignments",
            "priority": "high",
            "category_id": category_id
        }
    )

    # Search for "groceries"
    response = client.get("/api/v1/todos/?search=groceries")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert "groceries" in data["items"][0]["title"].lower()


def test_get_overdue_todos(client):
    """Test getting overdue todos via API."""
    # Create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Work", "color": "#FF5733"}
    )
    category_id = category_response.json()["id"]

    # Create an overdue todo
    past_date = (datetime.now() - timedelta(days=1)).isoformat()
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Overdue task",
            "priority": "urgent",
            "due_date": past_date,
            "category_id": category_id
        }
    )

    # Create a future todo
    future_date = (datetime.now() + timedelta(days=7)).isoformat()
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Future task",
            "priority": "medium",
            "due_date": future_date,
            "category_id": category_id
        }
    )

    response = client.get("/api/v1/todos/overdue")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_upcoming_todos(client):
    """Test getting upcoming todos via API."""
    # Create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Personal", "color": "#3498DB"}
    )
    category_id = category_response.json()["id"]

    # Create an upcoming todo
    tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Task tomorrow",
            "priority": "medium",
            "due_date": tomorrow,
            "category_id": category_id
        }
    )

    response = client.get("/api/v1/todos/upcoming")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_statistics(client):
    """Test getting todo statistics via API."""
    # Create a category
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "Work", "color": "#FF5733"}
    )
    category_id = category_response.json()["id"]

    # Create various todos
    client.post(
        "/api/v1/todos/",
        json={"title": "Task 1", "priority": "low", "category_id": category_id}
    )
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Task 2",
            "priority": "medium",
            "completed": True,
            "category_id": category_id
        }
    )

    # Create an overdue todo
    past_date = (datetime.now() - timedelta(days=1)).isoformat()
    client.post(
        "/api/v1/todos/",
        json={
            "title": "Overdue task",
            "priority": "urgent",
            "due_date": past_date,
            "category_id": category_id
        }
    )

    response = client.get("/api/v1/todos/statistics")

    assert response.status_code == 200
    stats = response.json()
    assert "total" in stats
    assert "completed" in stats
    assert "pending" in stats
    assert "overdue" in stats
    assert stats["total"] == 3


def test_create_todo_invalid_priority(client):
    """Test creating a todo with invalid priority."""
    response = client.post(
        "/api/v1/todos/",
        json={
            "title": "Test task",
            "priority": "invalid_priority"
        }
    )

    assert response.status_code == 422


def test_create_todo_missing_title(client):
    """Test creating a todo without title."""
    response = client.post(
        "/api/v1/todos/",
        json={
            "priority": "medium"
        }
    )

    assert response.status_code == 422


def test_get_nonexistent_todo(client):
    """Test getting a non-existent todo."""
    response = client.get("/api/v1/todos/99999")

    assert response.status_code == 404