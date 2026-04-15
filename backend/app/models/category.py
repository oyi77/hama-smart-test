"""
Category model following Single Responsibility Principle.
Handles category data structure and relationships.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Category(Base):
    """
    Category model for organizing todos.
    Follows Single Responsibility - only handles category data.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    color = Column(String(7), nullable=False)  # Hex color code
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', color='{self.color}')>"