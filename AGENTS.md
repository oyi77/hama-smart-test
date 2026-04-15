# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-15
**Commit:** b99403f
**Branch:** master

## OVERVIEW

TodoList desktop application — FastAPI (Python) backend + Electron/React/Vite frontend. SQLite persistence. Built as a live coding test project following SOLID/KISS principles.

## STRUCTURE

```
hama-smart-test/
├── backend/        # FastAPI REST API (Python, SQLAlchemy, Pydantic)
├── desktop/        # Electron app (React, Vite, Tailwind, vanilla JS)
├── start_all.sh    # One-command launcher (venv + deps + both servers)
├── PLAN.md         # Software Design Document (full spec)
└── req.txt         # Backup requirements
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add API endpoint | `backend/app/api/v1/` | Create router file, register in `main.py` |
| Add DB model | `backend/app/models/` | Create model file, import in `models/__init__.py` |
| Add Pydantic schema | `backend/app/schemas/` | Separate Create/Update/Response schemas |
| Add CRUD logic | `backend/app/crud/` | Repository class pattern, factory function |
| Add UI component | `desktop/src/renderer/` | Vanilla JS (no JSX), see PLAN.md structure |
| Modify IPC bridge | `desktop/src/main/index.js` | ipcMain.handle channels |
| Change DB config | `backend/app/core/config.py` + `core/database.py` | Settings via pydantic-settings |
| Run tests | `backend/tests/` | pytest with SQLite test DB per function |

## CONVENTIONS

- **Dual codebase**: Flat legacy files (`app/crud.py`, `app/models.py`, `app/schemas.py`, `app/database.py`, `app/router.py`) coexist with modular subpackages (`app/crud/`, `app/models/`, `app/schemas/`, `app/core/`, `app/api/v1/`). The **modular subpackages are the active implementation**. Flat files are legacy.
- **Backend pattern**: Models → Schemas (Pydantic) → CRUD (Repository class) → API router (v1). Factory functions for DI.
- **Frontend pattern**: Renderer (React/Vite) → IPC (ipcMain in main process) → FastAPI via fetch. API client abstracts IPC.
- **No TypeScript** on frontend — all `.js` files.
- **No linter/formatter configs** present.

## ANTI-PATTERNS (THIS PROJECT)

- **Do NOT** modify flat legacy files (`crud.py`, `models.py`, `schemas.py`, `router.py`, `database.py`) — they are superseded by subpackage versions.
- **Do NOT** import from `app.database` (legacy) — use `app.core.database`.
- `conftest.py` imports `app.models` and `app.schemas` directly but shadows them with local variables — watch for naming collisions.
- Backend API returns `TodoListResponse` with `items`/`total`/`page`/`page_size` for list endpoints — not plain arrays.
- `requirements.txt` has `pydantic` listed twice.

## COMMANDS

```bash
# Start everything
./start_all.sh

# Backend only
cd backend && source venv/bin/activate
uvicorn app.main:app --reload --port 8000    # API at http://localhost:8000/docs

# Frontend only
cd desktop && npm install
npm run dev                                    # Vite :5173 + Electron

# Tests
cd backend && pytest --cov=app tests/ -v
cd desktop && npm test                          # vitest
```

## NOTES

- SQLite DB file (`todolist.db`) created at `backend/` cwd on first run. Test DB (`test.db`) created in `backend/tests/`.
- Electron `nodeIntegration: true` + `contextIsolation: false` — not secure for production, fine for desktop test project.
- `main.py` uses deprecated `@app.on_event("startup")` — should use lifespan in future.
- `start_all.sh` creates venv at `backend/venv/` if missing.
- API prefix: `/api/v1` — all endpoints under this path.
