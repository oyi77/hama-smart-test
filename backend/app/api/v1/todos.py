"""
Todo API endpoints following Single Responsibility Principle.
Handles todo-related HTTP requests and responses.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, Priority
from app.crud.todo import get_todo_repository

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new todo.
    Follows KISS Principle - simple, focused endpoint.
    """
    repo = get_todo_repository(db)
    try:
        todo = repo.create(todo_data)
        return todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=TodoListResponse)
def get_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    completed: Optional[bool] = Query(None),
    priority: Optional[Priority] = Query(None),
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    """
    Get todos with filtering, pagination, and search.
    Supports filtering by completion status, priority, and category.
    """
    repo = get_todo_repository(db)
    todos = repo.get_all(
        skip=skip,
        limit=limit,
        completed=completed,
        priority=priority,
        category_id=category_id,
        search=search
    )
    total = len(todos)  # In production, you'd want a separate count query
    return TodoListResponse(
        items=todos,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/overdue", response_model=List[TodoResponse])
def get_overdue_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all overdue and incomplete todos."""
    repo = get_todo_repository(db)
    return repo.get_overdue(skip=skip, limit=limit)


@router.get("/upcoming", response_model=List[TodoResponse])
def get_upcoming_todos(
    days: int = Query(7, ge=1, le=30),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get todos due within the specified number of days."""
    repo = get_todo_repository(db)
    return repo.get_upcoming(days=days, skip=skip, limit=limit)


@router.get("/statistics", response_model=dict)
def get_todo_statistics(db: Session = Depends(get_db)):
    """Get todo statistics including total, completed, pending, and overdue counts."""
    repo = get_todo_repository(db)
    return repo.get_statistics()


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID."""
    repo = get_todo_repository(db)
    todo = repo.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing todo."""
    repo = get_todo_repository(db)
    todo = repo.update(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo."""
    repo = get_todo_repository(db)
    success = repo.delete(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None
