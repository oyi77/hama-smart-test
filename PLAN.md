# Software Design Document (SDD): TodoList Desktop Application

**Version:** 1.0  
**Date:** 2026-04-15  
**Tech Stack:** Electron (Frontend) + FastAPI (Backend) + SQLite

---

## 1. Introduction

### 1.1 Purpose
Build a desktop TodoList application with modern, user-friendly UI supporting complete task management.

### 1.2 Scope
**Core Features:**
- List, Add, Update, Delete todos
- Categories with color coding
- Priority levels (Low/Medium/High/Urgent)
- Due dates with visual indicators
- Reminders via desktop notifications
- Search and filter functionality

### 1.3 Constraints
- Desktop-only (Electron)
- SQLite for data persistence
- SOLID + KISS principles
- >90% backend test coverage, >80% frontend coverage

---

## 2. System Overview

### 2.1 Architecture
```
┌─────────────────┐     HTTP/REST      ┌─────────────────┐
│   Electron App  │ ◄─────────────────► │  FastAPI Server │
│   (Renderer)    │                     │   Port: 8000    │
└────────┬────────┘                     └────────┬────────┘
         │                                        │
         │ IPC                                   │ SQLAlchemy
         ▼                                        ▼
┌─────────────────┐                     ┌─────────────────┐
│  Main Process   │                     │     SQLite      │
│  (Node.js)      │                     │   (Local DB)    │
└─────────────────┘                     └─────────────────┘
```

### 2.2 Project Structure
```
hama-smart-test/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry
│   │   ├── core/
│   │   │   ├── config.py      # Settings
│   │   │   └── database.py    # DB connection
│   │   ├── models/
│   │   │   ├── todo.py
│   │   │   └── category.py
│   │   ├── schemas/
│   │   │   ├── todo.py
│   │   │   └── category.py
│   │   ├── crud/
│   │   │   ├── todo.py
│   │   │   └── category.py
│   │   └── api/
│   │       └── v1/
│   │           ├── todos.py
│   │           └── categories.py
│   ├── tests/
│   └── requirements.txt
├── desktop/                    # Electron Frontend
│   ├── src/
│   │   ├── main/
│   │   │   ├── index.js       # Entry point
│   │   │   ├── window.js      # Window mgmt
│   │   │   └── preload.js     # IPC bridge
│   │   ├── renderer/
│   │   │   ├── index.html
│   │   │   ├── styles.css
│   │   │   ├── app.js
│   │   │   └── components/
│   │   │       ├── TodoList.js
│   │   │       ├── TodoItem.js
│   │   │       ├── TodoForm.js
│   │   │       ├── CategoryManager.js
│   │   │       └── SearchFilter.js
│   │   └── shared/
│   │       └── api-client.js
│   ├── tests/
│   └── package.json
└── README.md
```

---

## 3. Data Design

### 3.1 Database Schema

```sql
-- Category Table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(7) DEFAULT '#3B82F6',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Todo Table
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(10) DEFAULT 'medium', -- low/medium/high/urgent
    due_date TIMESTAMP,
    reminder_at TIMESTAMP,
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### 3.2 Models (SQLAlchemy)

**Category Model:**
- `id`: Integer, PK
- `name`: String, unique
- `color`: String (hex color)
- `created_at`: DateTime

**Todo Model:**
- `id`: Integer, PK
- `title`: String(200), required
- `description`: Text, optional
- `completed`: Boolean, default False
- `priority`: Enum(low/medium/high/urgent)
- `due_date`: DateTime, optional
- `reminder_at`: DateTime, optional
- `category_id`: FK to Category
- `created_at`: DateTime
- `updated_at`: DateTime

---

## 4. API Design

### 4.1 Base URL
```
http://localhost:8000/api/v1
```

### 4.2 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos` | List todos (with filters) |
| POST | `/todos` | Create new todo |
| GET | `/todos/{id}` | Get single todo |
| PUT | `/todos/{id}` | Update todo |
| DELETE | `/todos/{id}` | Delete todo |
| GET | `/categories` | List categories |
| POST | `/categories` | Create category |
| PUT | `/categories/{id}` | Update category |
| DELETE | `/categories/{id}` | Delete category |

### 4.3 Query Parameters (GET /todos)
```
GET /todos?completed=false&priority=high&category_id=1&search=keyword&due_before=2026-04-30
```

### 4.4 Request/Response Schemas

**Create Todo:**
```json
POST /todos
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "due_date": "2026-04-16T10:00:00",
  "category_id": 1
}
```

**Todo Response:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "medium",
  "due_date": "2026-04-16T10:00:00",
  "category_id": 1,
  "category": {
    "id": 1,
    "name": "Personal",
    "color": "#3B82F6"
  },
  "created_at": "2026-04-15T08:00:00",
  "updated_at": "2026-04-15T08:00:00"
}
```

---

## 5. UI Design

### 5.1 Layout
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Search...    [Filter ▼]    [+ New Todo]                │
├──────────┬──────────────────────────────────────────────────┤
│          │  📋 My Todos                                    │
│ Categories│                                                  │
│ ─────────│  ┌─────────────────────────────────────────────┐  │
│ 🔵 All   │  │ ☐ Buy groceries                    [⋮]   │  │
│ 🟢 Work  │  │    🟢 Work • Due today • Medium priority    │  │
│ 🔴 Urgent│  └─────────────────────────────────────────────┘  │
│ 🟡 Shop  │  ┌─────────────────────────────────────────────┐  │
│          │  │ ☑ Call dentist (done)                [⋮]   │  │
│──────────│  │    🔴 Urgent • Completed                      │  │
│ Priorities└─────────────────────────────────────────────┘  │
│ ⭐ Urgent│                                                  │
│ 🔴 High  │  ┌─────────────────────────────────────────────┐  │
│ 🟡 Medium│  │ ☐ Submit report                    [⋮]   │  │
│ 🟢 Low   │  │    🟢 Work • Due tomorrow • High priority │  │
│          │  └─────────────────────────────────────────────┘  │
└──────────┴──────────────────────────────────────────────────┘
```

### 5.2 Key UI Components

| Component | Purpose |
|-----------|---------|
| Sidebar | Category list + Priority filters |
| Search Bar | Real-time search with debounce |
| Filter Dropdown | Status, date range filters |
| Todo List | Scrollable list of todo items |
| Todo Item | Checkbox, title, metadata, actions |
| Todo Form | Modal for add/edit with validation |
| Category Manager | CRUD for categories with color picker |
| Notification | Toast for actions + native reminders |

### 5.3 Design Principles
- **Minimalist:** Clean whitespace, no clutter
- **Modern:** Rounded corners, subtle shadows
- **Accessible:** Proper contrast, keyboard navigation
- **Responsive:** Flexible layout for window resizing

---

## 6. Implementation Phases

### Phase 1: Backend Foundation
| Task | File | Time Est. |
|------|------|-----------|
| Setup FastAPI project | `backend/requirements.txt`, `main.py` | 30m |
| Database config | `core/database.py`, `config.py` | 30m |
| Create models | `models/todo.py`, `models/category.py` | 45m |
| Create schemas | `schemas/todo.py`, `schemas/category.py` | 45m |
| CRUD operations | `crud/todo.py`, `crud/category.py` | 1h |
| API endpoints | `api/v1/todos.py`, `api/v1/categories.py` | 1h |
| **Subtotal** | | **~4h** |

### Phase 2: Frontend Core
| Task | File | Time Est. |
|------|------|-----------|
| Setup Electron | `desktop/package.json`, `main/index.js` | 30m |
| Create window | `main/window.js` | 30m |
| IPC bridge | `main/preload.js` | 30m |
| API client | `shared/api-client.js` | 45m |
| HTML/CSS shell | `renderer/index.html`, `styles.css` | 1h |
| Main app logic | `renderer/app.js` | 1h |
| **Subtotal** | | **~4h** |

### Phase 3: UI Components
| Task | File | Time Est. |
|------|------|-----------|
| TodoList component | `components/TodoList.js` | 45m |
| TodoItem component | `components/TodoItem.js` | 45m |
| TodoForm component | `components/TodoForm.js` | 1h |
| CategoryManager | `components/CategoryManager.js` | 1h |
| SearchFilter | `components/SearchFilter.js` | 45m |
| **Subtotal** | | **~4.5h** |

### Phase 4: Advanced Features
| Task | Description | Time Est. |
|------|-------------|-----------|
| Reminder system | Native notifications + background checks | 1.5h |
| Due date styling | Visual indicators for overdue/upcoming | 45m |
| Search & filter | Real-time search + multi-filter | 1h |
| **Subtotal** | | **~3h** |

### Phase 5: Testing
| Task | Files | Time Est. |
|------|-------|-----------|
| Backend tests | `tests/test_*.py` | 2h |
| Frontend tests | `tests/*.test.js` | 1.5h |
| E2E tests | Integration tests | 1h |
| **Subtotal** | | **~4.5h** |

**Total Estimated Time: ~20 hours**

---

## 7. Testing Strategy

### 7.1 Backend Tests (pytest)
```python
# Key test files:
- tests/test_models.py      # Model validation
- tests/test_crud_todo.py   # Database operations
- tests/test_api_todos.py   # API endpoints
- tests/conftest.py         # Fixtures
```

**Coverage Goals:**
- Models: 100%
- CRUD: 95%
- API: 90%

### 7.2 Frontend Tests (Jest)
```javascript
// Key test files:
- tests/components/TodoList.test.js
- tests/components/TodoForm.test.js
- tests/shared/api-client.test.js
```

**Coverage Goals:**
- Components: 85%
- Utilities: 90%

### 7.3 E2E Tests
- Create todo flow
- Edit todo flow
- Delete todo flow
- Filter and search
- Category management

### 7.4 Validation Commands
```bash
# Backend
cd backend
pytest --cov=app tests/ -v          # Run with coverage
pytest tests/test_api_todos.py -v    # API tests only

# Frontend
cd desktop
npm test                             # Unit tests
npm run test:e2e                     # E2E tests

# Integration
cd desktop && npm run build          # Build test
```

---

## 8. Design Principles Application

### SOLID
| Principle | Application |
|-----------|-------------|
| **S**ingle Responsibility | Each module has one job: models define data, CRUD handles DB, API handles HTTP |
| **O**pen/Closed | Use base classes; extend for new features without modifying existing code |
| **L**iskov Substitution | Repository pattern allows swapping SQLite for other DB |
| **I**nterface Segregation | Separate schemas for create/read/update operations |
| **D**ependency Inversion | API depends on CRUD abstractions, not concrete DB |

### KISS
- Use simple REST API (no GraphQL)
- SQLite over PostgreSQL (no external deps)
- Basic Electron setup (no complex build tools)
- Vanilla JS or minimal framework (no React/Vue unless needed)
- Simple error handling (don't over-engineer)

---

## 9. Critical Implementation Files

### Must Create (Backend)
```
backend/app/main.py
backend/app/core/database.py
backend/app/core/config.py
backend/app/models/todo.py
backend/app/schemas/todo.py
backend/app/crud/todo.py
backend/app/api/v1/todos.py
backend/tests/conftest.py
backend/requirements.txt
```

### Must Create (Frontend)
```
desktop/src/main/index.js
desktop/src/main/preload.js
desktop/src/renderer/index.html
desktop/src/renderer/styles.css
desktop/src/renderer/app.js
desktop/src/renderer/components/TodoList.js
desktop/src/shared/api-client.js
desktop/package.json
```

---

## 10. Success Criteria

- [ ] All CRUD operations working
- [ ] Categories with colors implemented
- [ ] Priority levels (Low/Medium/High/Urgent)
- [ ] Due dates with visual indicators
- [ ] Reminder notifications working
- [ ] Search and filter functional
- [ ] Backend coverage >90%
- [ ] Frontend coverage >80%
- [ ] SOLID principles followed
- [ ] KISS principles applied
- [ ] App builds successfully
- [ ] Manual testing passed

---

## 11. Quick Reference

**Start Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

**Start Frontend:**
```bash
cd desktop
npm install
npm start
```

**Run Tests:**
```bash
cd backend && pytest -v
cd desktop && npm test
```

---

*End of SDD*
