from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: Optional[bool] = False
    category: Optional[str] = "General"

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    category: Optional[str] = None

class Todo(TodoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
