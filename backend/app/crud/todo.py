"""
Todo CRUD operations following Repository Pattern.
Separates data access logic from business logic.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.todo import Todo, Priority
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    """
    Repository for todo data access.
    Follows Single Responsibility - only handles todo CRUD.
    """

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo."""
        db_todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            due_date=todo_data.due_date,
            category_id=todo_data.category_id
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def get(self, todo_id: int) -> Optional[Todo]:
        """Get todo by ID."""
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[Priority] = None,
        category_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Todo]:
        """Get todos with filtering and pagination."""
        query = self.db.query(Todo)

        # Apply filters
        if completed is not None:
            query = query.filter(Todo.completed == completed)

        if priority is not None:
            query = query.filter(Todo.priority == priority)

        if category_id is not None:
            query = query.filter(Todo.category_id == category_id)

        if search:
            query = query.filter(
                or_(
                    Todo.title.ilike(f"%{search}%"),
                    Todo.description.ilike(f"%{search}%")
                )
            )

        # Order by created date (newest first) and apply pagination
        return query.order_by(Todo.created_at.desc()).offset(skip).limit(limit).all()

    def update(self, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo."""
        db_todo = self.get(todo_id)
        if not db_todo:
            return None

        update_data = todo_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def delete(self, todo_id: int) -> bool:
        """Delete a todo."""
        db_todo = self.get(todo_id)
        if not db_todo:
            return False

        self.db.delete(db_todo)
        self.db.commit()
        return True

    def get_overdue(self, skip: int = 0, limit: int = 100) -> List[Todo]:
        """Get all overdue and incomplete todos."""
        return self.db.query(Todo).filter(
            and_(
                Todo.due_date < datetime.now(),
                Todo.completed == False
            )
        ).order_by(Todo.due_date.asc()).offset(skip).limit(limit).all()

    def get_upcoming(self, days: int = 7, skip: int = 0, limit: int = 100) -> List[Todo]:
        """Get todos due within the specified number of days."""
        future_date = datetime.now().replace(hour=23, minute=59, second=59)
        future_date = future_date.replace(day=future_date.day + days)

        return self.db.query(Todo).filter(
            and_(
                Todo.due_date >= datetime.now(),
                Todo.due_date <= future_date,
                Todo.completed == False
            )
        ).order_by(Todo.due_date.asc()).offset(skip).limit(limit).all()

    def get_statistics(self) -> dict:
        """Get todo statistics."""
        total = self.db.query(Todo).count()
        completed = self.db.query(Todo).filter(Todo.completed == True).count()
        pending = total - completed

        overdue = self.db.query(Todo).filter(
            and_(
                Todo.due_date < datetime.now(),
                Todo.completed == False
            )
        ).count()

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue
        }


def get_todo_repository(db: Session) -> TodoRepository:
    """
    Factory function for todo repository.
    Follows Dependency Inversion Principle.
    """
    return TodoRepository(db)