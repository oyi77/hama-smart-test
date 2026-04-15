# DESKTOP — Electron + React/Vite Frontend

## OVERVIEW

Electron desktop app with React UI (Vite dev server) communicating with FastAPI backend via IPC. Vanilla JS, no TypeScript.

## STRUCTURE

```
desktop/
├── main.js              # Electron entry — calls window.js + notification setup
├── package.json         # Scripts: dev (vite+electron), dev:react, dev:electron, test (vitest)
├── src/
│   ├── main/
│   │   ├── index.js     # App lifecycle + ALL ipcMain.handle handlers (proxy to FastAPI)
│   │   ├── window.js    # BrowserWindow creation + notification handler setup
│   │   ├── preload.js   # contextBridge (currently unused — nodeIntegration=true)
│   │   └── api-client.js # IPC wrapper class (ipcRenderer.invoke) — singleton export
│   ├── renderer/        # React UI (loaded from Vite :5173 in dev)
│   └── shared/
│       └── api-client.js # Duplicate of main/api-client.js (likely for renderer use)
├── tests/               # Vitest test files
└── package-lock.json
```

## WHERE TO LOOK

| Task | File | Notes |
|------|------|-------|
| Add IPC channel | `src/main/index.js` | Add `ipcMain.handle('<channel>', handler)` + method in `api-client.js` |
| Add API call | `src/main/api-client.js` | Add method to `APIClient` class, calls `this.invoke(channel)` |
| Change window config | `src/main/window.js` | BrowserWindow options |
| Add React component | `src/renderer/` | Vanilla JS, no JSX — use `React.createElement` or `.js` extension |
| Add test | `tests/` | Vitest, see existing patterns |

## CONVENTIONS

- **Communication flow**: Renderer → `ipcRenderer.invoke(channel)` → Main process (`ipcMain.handle`) → `fetch()` to FastAPI → response back via IPC.
- **IPC response shape**: Always `{ success: boolean, data?: any, error?: string }`.
- **API client**: Singleton `module.exports = new APIClient()`. Methods: `getTodos`, `createTodo`, `updateTodo`, `deleteTodo`, `getCategories`, `createCategory`, `updateCategory`, `deleteCategory`, `getStatistics`, `getOverdueTodos`, `getUpcomingTodos`.
- **Dev mode**: Vite serves on `:5173`, Electron loads that URL. Production loads `dist/index.html`.

## ANTI-PATTERNS

- `nodeIntegration: true` + `contextIsolation: false` — security risk in production, acceptable for desktop test project.
- `preload.js` exists but is not wired into BrowserWindow — dead code.
- `api-client.js` duplicated in `src/main/` and `src/shared/` — likely should be one file.
- `main.js` (root) and `src/main/index.js` are different files — `main.js` is the actual Electron entry point (`package.json` `"main": "main.js"`). `index.js` contains the IPC handlers but is required separately.

## COMMANDS

```bash
npm run dev          # Start Vite + Electron concurrently
npm run dev:react    # Vite dev server only (:5173)
npm run dev:electron # Electron only (expects Vite running)
npm run build        # Vite production build
npm test             # Vitest
```

## NOTES

- Backend must be running on `:8000` before Electron starts — IPC handlers fetch directly.
- No `.tsx` files — all React code is vanilla JS.
- `framer-motion` and `lucide-react` are dependencies but may not be fully utilized yet.
