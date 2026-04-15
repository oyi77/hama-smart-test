# APP PACKAGE — FastAPI Application Internals

## OVERVIEW

Core application package. Modular structure with legacy flat files alongside. Only use subpackage versions.

## ARCHITECTURE FLOW

```
main.py (FastAPI app setup, CORS, startup)
  ├── core/config.py → Settings singleton
  ├── core/database.py → engine, SessionLocal, Base, get_db()
  └── api/v1/ → routers mounted with prefix /api/v1
        ├── todos.py → TodoRepository (from crud/todo.py)
        └── categories.py → CategoryRepository (from crud/category.py)
```

## MODULE MAP

| Module | Responsibility | Key Exports |
|--------|---------------|-------------|
| `core/config.py` | App settings from env/.env | `settings` (Settings singleton) |
| `core/database.py` | SQLAlchemy engine + session | `engine`, `SessionLocal`, `Base`, `get_db()`, `init_db()` |
| `models/todo.py` | Todo ORM model + Priority enum | `Todo`, `Priority` |
| `models/category.py` | Category ORM model | `Category` |
| `schemas/todo.py` | Todo Pydantic schemas | `TodoCreate`, `TodoUpdate`, `TodoResponse`, `TodoListResponse` |
| `schemas/category.py` | Category Pydantic schemas | `CategoryCreate`, `CategoryUpdate`, `CategoryResponse`, `CategoryInTodo` |
| `crud/todo.py` | Todo repository + factory | `TodoRepository`, `get_todo_repository()` |
| `crud/category.py` | Category repository + factory | `CategoryRepository`, `get_category_repository()` |
| `api/v1/todos.py` | Todo HTTP endpoints | `router` (prefix=/todos) |
| `api/v1/categories.py` | Category HTTP endpoints | `router` (prefix=/categories) |

## ANTI-PATTERNS

- **Flat legacy files at root level** (`crud.py`, `models.py`, `schemas.py`, `router.py`, `database.py`): These are superseded. Do NOT import from them. Use subpackage versions only.
- `main.py` imports from `app.core.*` and `app.api.v1.*` — flat files are NOT wired in.

## NOTES

- `Base` from `core/database.py` is the ORM base class — all models inherit from it.
- `get_db()` is a FastAPI dependency (generator) — yields session, auto-closes.
- `init_db()` called on startup via deprecated `@app.on_event("startup")`.
- Todo-Cateory relationship: `todo.category_id` FK → `category.id`. ORM relationship `todo.category` gives eager-loaded Category object.
