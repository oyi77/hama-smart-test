"""
Todo schemas following Open/Closed Principle.
Open for extension, closed for modification through inheritance.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.schemas.category import CategoryInTodo
from enum import Enum


class Priority(str, Enum):
    """Priority type with validation."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TodoBase(BaseModel):
    """Base todo schema with common fields."""
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    priority: Priority = Field(default=Priority.MEDIUM, description="Todo priority")
    due_date: Optional[datetime] = Field(None, description="Due date for the todo")
    category_id: Optional[int] = Field(None, description="Category ID")

    @validator('due_date')
    def validate_due_date(cls, v):
        """Ensure due date is in the future if provided."""
        if v is not None and v < datetime.now():
            raise ValueError('Due date must be in the future')
        return v


class TodoCreate(TodoBase):
    """Schema for creating todos."""
    pass


class TodoUpdate(BaseModel):
    """Schema for updating todos - all fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None and v < datetime.now():
            raise ValueError('Due date must be in the future')
        return v


class TodoResponse(TodoBase):
    """Schema for todo responses."""
    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CategoryInTodo] = None

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema for paginated todo list responses."""
    items: list[TodoResponse]
    total: int
    page: int
    page_size: int