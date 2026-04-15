"""
Tests for todo CRUD operations.
Follows Single Responsibility Principle - only tests todo repository.
"""
import pytest
from datetime import datetime, timedelta
from app.crud.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate, Priority


def test_create_todo(db, sample_category):
    """Test creating a new todo."""
    repo = TodoRepository(db)
    todo_data = TodoCreate(
        title="Complete project",
        description="Finish the implementation",
        priority=Priority.HIGH,
        category_id=sample_category.id
    )

    todo = repo.create(todo_data)

    assert todo.id is not None
    assert todo.title == "Complete project"
    assert todo.completed is False
    assert todo.priority == Priority.HIGH


def test_get_todo(db, sample_todo):
    """Test retrieving a todo by ID."""
    repo = TodoRepository(db)

    todo = repo.get(sample_todo.id)

    assert todo is not None
    assert todo.id == sample_todo.id
    assert todo.title == sample_todo.title


def test_get_all_todos(db):
    """Test retrieving all todos."""
    repo = TodoRepository(db)

    # Create multiple todos
    repo.create(TodoCreate(title="First task", priority=Priority.LOW))
    repo.create(TodoCreate(title="Second task", priority=Priority.MEDIUM))
    repo.create(TodoCreate(title="Third task", priority=Priority.HIGH))

    todos = repo.get_all()

    assert len(todos) == 3


def test_get_todos_with_filters(db, sample_category):
    """Test retrieving todos with filters."""
    repo = TodoRepository(db)

    # Create todos with different states
    repo.create(TodoCreate(
        title="Completed task",
        priority=Priority.LOW,
        completed=True,
        category_id=sample_category.id
    ))
    repo.create(TodoCreate(
        title="Pending high priority",
        priority=Priority.HIGH,
        completed=False,
        category_id=sample_category.id
    ))

    # Filter by completed status
    completed_todos = repo.get_all(completed=True)
    pending_todos = repo.get_all(completed=False)

    assert len(completed_todos) == 1
    assert len(pending_todos) >= 1

    # Filter by priority
    high_priority_todos = repo.get_all(priority=Priority.HIGH)
    assert len(high_priority_todos) >= 1

    # Filter by category
    category_todos = repo.get_all(category_id=sample_category.id)
    assert len(category_todos) >= 1


def test_search_todos(db):
    """Test searching todos by title and description."""
    repo = TodoRepository(db)

    # Create todos
    repo.create(TodoCreate(
        title="Buy groceries",
        description="Milk, eggs, bread, and vegetables"
    ))
    repo.create(TodoCreate(
        title("Complete homework"),
        description="Math and science assignments"
    ))
    repo.create(TodoCreate(
        title="Go shopping",
        description="Buy new clothes"
    ))

    # Search for "shop"
    results = repo.get_all(search="shop")

    assert len(results) >= 2  # Should find both shopping-related todos


def test_update_todo(db, sample_todo):
    """Test updating a todo."""
    repo = TodoRepository(db)
    update_data = TodoUpdate(
        completed=True,
        priority=Priority.URGENT
    )

    updated_todo = repo.update(sample_todo.id, update_data)

    assert updated_todo is not None
    assert updated_todo.completed is True
    assert updated_todo.priority == Priority.URGENT


def test_delete_todo(db, sample_todo):
    """Test deleting a todo."""
    repo = TodoRepository(db)

    success = repo.delete(sample_todo.id)

    assert success is True
    assert repo.get(sample_todo.id) is None


def test_get_overdue_todos(db):
    """Test retrieving overdue todos."""
    repo = TodoRepository(db)

    # Create an overdue todo
    past_date = datetime.now() - timedelta(days=1)
    repo.create(TodoCreate(
        title="Overdue task",
        priority=Priority.HIGH,
        due_date=past_date
    ))

    # Create a future todo
    future_date = datetime.now() + timedelta(days=7)
    repo.create(TodoCreate(
        title="Future task",
        priority=Priority.MEDIUM,
        due_date=future_date
    ))

    overdue_todos = repo.get_overdue()

    assert len(overdue_todos) >= 1
    assert all(todo.due_date < datetime.now() for todo in overdue_todos)


def test_get_upcoming_todos(db):
    """Test retrieving upcoming todos."""
    repo = TodoRepository(db)

    # Create todos with different due dates
    tomorrow = datetime.now() + timedelta(days=1)
    next_week = datetime.now() + timedelta(days=7)
    next_month = datetime.now() + timedelta(days=30)

    repo.create(TodoCreate(
        title="Task tomorrow",
        priority=Priority.MEDIUM,
        due_date=tomorrow
    ))
    repo.create(TodoCreate(
        title="Task next week",
        priority=Priority.LOW,
        due_date=next_week
    ))
    repo.create(TodoCreate(
        title="Task next month",
        priority=Priority.HIGH,
        due_date=next_month
    ))

    # Get todos due within next 7 days
    upcoming_todos = repo.get_upcoming(days=7)

    assert len(upcoming_todos) >= 1
    assert all(todo.due_date >= datetime.now() for todo in upcoming_todos)


def test_get_statistics(db):
    """Test retrieving todo statistics."""
    repo = TodoRepository(db)

    # Create various todos
    repo.create(TodoCreate(title="Task 1", priority=Priority.LOW))
    repo.create(TodoCreate(title="Task 2", priority=Priority.MEDIUM, completed=True))
    repo.create(TodoCreate(title="Task 3", priority=Priority.HIGH))

    # Create an overdue todo
    past_date = datetime.now() - timedelta(days=1)
    repo.create(TodoCreate(
        title="Overdue task",
        priority=Priority.URGENT,
        due_date=past_date
    ))

    stats = repo.get_statistics()

    assert stats["total"] == 4
    assert stats["completed"] == 1
    assert stats["pending"] == 3
    assert stats["overdue"] == 1


def test_get_nonexistent_todo(db):
    """Test retrieving a non-existent todo."""
    repo = TodoRepository(db)

    todo = repo.get(99999)

    assert todo is None


def test_update_nonexistent_todo(db):
    """Test updating a non-existent todo."""
    repo = TodoRepository(db)
    update_data = TodoUpdate(title="Updated")

    todo = repo.update(99999, update_data)

    assert todo is None


def test_delete_nonexistent_todo(db):
    """Test deleting a non-existent todo."""
    repo = TodoRepository(db)

    success = repo.delete(99999)

    assert success is False