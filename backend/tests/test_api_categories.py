"""
Tests for category API endpoints.
Follows Single Responsibility Principle - only tests category API.
"""
from fastapi.testclient import TestClient


def test_create_category(client):
    """Test creating a category via API."""
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Work",
            "color": "#FF5733"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Work"
    assert data["color"] == "#FF5733"
    assert "id" in data


def test_get_categories(client):
    """Test getting all categories via API."""
    # Create some categories first
    client.post("/api/v1/categories/", json={"name": "Work", "color": "#FF5733"})
    client.post("/api/v1/categories/", json={"name": "Personal", "color": "#3498DB"})

    response = client.get("/api/v1/categories/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_category(client):
    """Test getting a specific category via API."""
    # Create a category first
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Shopping", "color": "#2ECC71"}
    )
    category_id = create_response.json()["id"]

    response = client.get(f"/api/v1/categories/{category_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Shopping"


def test_update_category(client):
    """Test updating a category via API."""
    # Create a category first
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Old Name", "color": "#FF0000"}
    )
    category_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/categories/{category_id}",
        json={
            "name": "Updated Name",
            "color": "#00FF00"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["color"] == "#00FF00"


def test_delete_category(client):
    """Test deleting a category via API."""
    # Create a category first
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "To Delete", "color": "#FF0000"}
    )
    category_id = create_response.json()["id"]

    response = client.delete(f"/api/v1/categories/{category_id}")

    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/api/v1/categories/{category_id}")
    assert get_response.status_code == 404


def test_search_categories(client):
    """Test searching categories via API."""
    # Create categories
    client.post("/api/v1/categories/", json={"name": "Work Project", "color": "#FF5733"})
    client.post("/api/v1/categories/", json={"name": "Personal Tasks", "color": "#3498DB"})

    response = client.get("/api/v1/categories/?search=work")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "work" in data[0]["name"].lower()


def test_create_category_invalid_color(client):
    """Test creating a category with invalid color."""
    response = client.post(
        "/api/v1/categories/",
        json={
            "name": "Invalid Color",
            "color": "invalid"
        }
    )

    assert response.status_code == 422


def test_create_category_missing_name(client):
    """Test creating a category without name."""
    response = client.post(
        "/api/v1/categories/",
        json={
            "color": "#FF5733"
        }
    )

    assert response.status_code == 422


def test_get_nonexistent_category(client):
    """Test getting a non-existent category."""
    response = client.get("/api/v1/categories/99999")

    assert response.status_code == 404