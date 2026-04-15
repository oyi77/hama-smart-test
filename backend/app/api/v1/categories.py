"""
Category API endpoints following Single Responsibility Principle.
Handles category-related HTTP requests and responses.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.crud.category import get_category_repository

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new category.
    Follows KISS Principle - simple, focused endpoint.
    """
    repo = get_category_repository(db)
    try:
        category = repo.create(category_data)
        return category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str = Query(None, min_length=1),
    db: Session = Depends(get_db)
):
    """
    Get all categories with optional pagination and search.
    """
    repo = get_category_repository(db)
    if search:
        return repo.search(search, skip=skip, limit=limit)
    return repo.get_all(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID."""
    repo = get_category_repository(db)
    category = repo.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing category."""
    repo = get_category_repository(db)
    category = repo.update(category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category."""
    repo = get_category_repository(db)
    success = repo.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None