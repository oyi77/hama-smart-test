"""
Category CRUD operations following Repository Pattern.
Separates data access logic from business logic.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    """
    Repository for category data access.
    Follows Single Responsibility - only handles category CRUD.
    """

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, category_data: CategoryCreate) -> Category:
        """Create a new category."""
        db_category = Category(
            name=category_data.name,
            color=category_data.color
        )
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def get(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        """Get all categories with pagination."""
        return self.db.query(Category).offset(skip).limit(limit).all()

    def update(self, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        """Update an existing category."""
        db_category = self.get(category_id)
        if not db_category:
            return None

        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)

        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def delete(self, category_id: int) -> bool:
        """Delete a category."""
        db_category = self.get(category_id)
        if not db_category:
            return False

        self.db.delete(db_category)
        self.db.commit()
        return True

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Category]:
        """Search categories by name."""
        return self.db.query(Category).filter(
            or_(
                Category.name.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()


def get_category_repository(db: Session) -> CategoryRepository:
    """
    Factory function for category repository.
    Follows Dependency Inversion Principle.
    """
    return CategoryRepository(db)