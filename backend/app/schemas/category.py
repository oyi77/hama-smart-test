"""
Category schemas following Open/Closed Principle.
Open for extension, closed for modification through inheritance.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema with common fields."""
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$', description="Hex color code")

    @validator('color')
    def validate_color(cls, v):
        """Validate color format."""
        if not v.startswith('#'):
            raise ValueError('Color must start with #')
        if len(v) != 7:
            raise ValueError('Color must be 7 characters (including #)')
        return v.upper()


class CategoryCreate(CategoryBase):
    """Schema for creating categories."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating categories - all fields optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')

    @validator('color')
    def validate_color(cls, v):
        if v is not None:
            if not v.startswith('#'):
                raise ValueError('Color must start with #')
            if len(v) != 7:
                raise ValueError('Color must be 7 characters (including #)')
            return v.upper()
        return v


class CategoryResponse(CategoryBase):
    """Schema for category responses."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryInTodo(BaseModel):
    """Minimal category info for todo responses."""
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True