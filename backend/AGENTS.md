# BACKEND — FastAPI TodoList API

## OVERVIEW

Python REST API using FastAPI + SQLAlchemy + Pydantic. SQLite persistence. Repository pattern for CRUD, factory functions for DI.

## STRUCTURE

```
backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, router includes, startup event
│   ├── crud.py          # Legacy flat CRUD — DO NOT USE
│   ├── models.py        # Legacy flat model — DO NOT USE
│   ├── schemas.py       # Legacy flat schemas — DO NOT USE
│   ├── database.py      # Legacy DB config — DO NOT USE (use core/database.py)
│   ├── router.py        # Legacy router — DO NOT USE
│   ├── core/
│   │   ├── config.py    # Settings (pydantic-settings, .env support)
│   │   └── database.py  # Engine, SessionLocal, Base, get_db(), init_db()
│   ├── models/
│   │   ├── todo.py      # Todo model + Priority enum
│   │   └── category.py  # Category model
│   ├── schemas/
│   │   ├── todo.py      # TodoBase/Create/Update/Response/ListResponse + Priority
│   │   └── category.py  # CategoryBase/Create/Update/Response/InTodo
│   ├── crud/
│   │   ├── todo.py      # TodoRepository class (create/get/get_all/update/delete/overdue/upcoming/stats)
│   │   └── category.py  # CategoryRepository class (create/get/get_all/update/delete/search)
│   └── api/v1/
│       ├── todos.py      # /todos router — CRUD + overdue/upcoming/statistics
│       └── categories.py # /categories router — CRUD + search
├── tests/
│   ├── conftest.py       # Fixtures: db, client, sample_category, sample_todo
│   ├── test_api.py       # Tests against legacy flat router
│   ├── test_crud_todo.py # Todo CRUD unit tests
│   ├── test_crud_category.py # Category CRUD unit tests
│   ├── test_api_todos.py # Todo API integration tests
│   └── test_api_categories.py # Category API integration tests
└── requirements.txt
```

## WHERE TO LOOK

| Task | File | Pattern |
|------|------|---------|
| New entity | `models/<name>.py` → `schemas/<name>.py` → `crud/<name>.py` → `api/v1/<name>.py` | Follow existing pattern |
| Change settings | `app/core/config.py` | `Settings(BaseSettings)` with env vars |
| Change DB engine | `app/core/database.py` | SQLite connect_args for thread safety |
| Add test fixture | `tests/conftest.py` | function-scoped, fresh DB per test |

## CONVENTIONS

- **Repository pattern**: CRUD classes take `db: Session` in constructor. Factory function `get_<entity>_repository(db)` for DI.
- **Schema hierarchy**: `*Base` → `*Create` (inherits Base) → `*Update` (all Optional) → `*Response` (adds id, timestamps). Separate `*InTodo` for nested relations.
- **API pattern**: Router with `prefix="/<entity>"`. DELETE returns 204 (not body). POST returns 201.
- **Color validation**: Hex `#RRGGBB` with regex + uppercase normalization.
- **Pagination**: `skip`/`limit` query params. `TodoListResponse` wraps list results.

## NOTES

- `conftest.py` fixture `sample_category` has a bug: `category.Category(...)` shadows the imported module. Works but fragile.
- Test DB is `sqlite:///./test.db` — created in `backend/` working directory.
- `TodoRepository.get_upcoming()` has a naive date calc that fails at month boundaries.
