"""
Tests for category CRUD operations.
Follows Single Responsibility Principle - only tests category repository.
"""
import pytest
from app.crud.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


def test_create_category(db):
    """Test creating a new category."""
    repo = CategoryRepository(db)
    category_data = CategoryCreate(name="Personal", color="#3498DB")

    category = repo.create(category_data)

    assert category.id is not None
    assert category.name == "Personal"
    assert category.color == "#3498DB"


def test_get_category(db, sample_category):
    """Test retrieving a category by ID."""
    repo = CategoryRepository(db)

    category = repo.get(sample_category.id)

    assert category is not None
    assert category.id == sample_category.id
    assert category.name == sample_category.name


def test_get_all_categories(db):
    """Test retrieving all categories."""
    repo = CategoryRepository(db)

    # Create multiple categories
    repo.create(CategoryCreate(name="Work", color="#FF5733"))
    repo.create(CategoryCreate(name="Personal", color="#3498DB"))
    repo.create(CategoryCreate(name="Shopping", color="#2ECC71"))

    categories = repo.get_all()

    assert len(categories) == 3


def test_update_category(db, sample_category):
    """Test updating a category."""
    repo = CategoryRepository(db)
    update_data = CategoryUpdate(name="Updated Work", color="#E74C3C")

    updated_category = repo.update(sample_category.id, update_data)

    assert updated_category is not None
    assert updated_category.name == "Updated Work"
    assert updated_category.color == "#E74C3C"


def test_delete_category(db, sample_category):
    """Test deleting a category."""
    repo = CategoryRepository(db)

    success = repo.delete(sample_category.id)

    assert success is True
    assert repo.get(sample_category.id) is None


def test_search_categories(db):
    """Test searching categories by name."""
    repo = CategoryRepository(db)

    # Create categories
    repo.create(CategoryCreate(name="Work Project", color="#FF5733"))
    repo.create(CategoryCreate(name="Personal Tasks", color="#3498DB"))
    repo.create(CategoryCreate(name="Shopping List", color="#2ECC71"))

    # Search for "work"
    results = repo.search("work")

    assert len(results) == 1
    assert "work" in results[0].name.lower()


def test_get_nonexistent_category(db):
    """Test retrieving a non-existent category."""
    repo = CategoryRepository(db)

    category = repo.get(99999)

    assert category is None


def test_update_nonexistent_category(db):
    """Test updating a non-existent category."""
    repo = CategoryRepository(db)
    update_data = CategoryUpdate(name="Updated")

    category = repo.update(99999, update_data)

    assert category is None


def test_delete_nonexistent_category(db):
    """Test deleting a non-existent category."""
    repo = CategoryRepository(db)

    success = repo.delete(99999)

    assert success is False