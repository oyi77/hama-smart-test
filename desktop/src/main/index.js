/**
 * Electron main process entry point.
 * Follows Single Responsibility Principle - handles Electron app lifecycle.
 */
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

let mainWindow;

/**
 * Create the main browser window.
 * Follows KISS Principle - simple window creation.
 */
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#ffffff',
  });

  // Load the app
  const startUrl = isDev
    ? 'http://localhost:5173' // Vite dev server
    : `file://${path.join(__dirname, '../dist/index.html')}`; // Production build

  mainWindow.loadURL(startUrl);

  // Open DevTools in development
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

/**
 * App lifecycle events.
 */
app.on('ready', () => {
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

/**
 * IPC handlers for backend communication.
 * Follows Single Responsibility - each handler has one purpose.
 */

// Get all todos
ipcMain.handle('get-todos', async (event, filters = {}) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/todos/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Create todo
ipcMain.handle('create-todo', async (event, todoData) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/todos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todoData),
    });
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Update todo
ipcMain.handle('update-todo', async (event, id, todoData) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/todos/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(todoData),
    });
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Delete todo
ipcMain.handle('delete-todo', async (event, id) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/todos/${id}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      return { success: true };
    } else {
      return { success: false, error: 'Failed to delete todo' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get categories
ipcMain.handle('get-categories', async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/categories/');
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Create category
ipcMain.handle('create-category', async (event, categoryData) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/categories/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(categoryData),
    });
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Update category
ipcMain.handle('update-category', async (event, id, categoryData) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/categories/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(categoryData),
    });
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Delete category
ipcMain.handle('delete-category', async (event, id) => {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/categories/${id}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      return { success: true };
    } else {
      return { success: false, error: 'Failed to delete category' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get todo statistics
ipcMain.handle('get-statistics', async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/todos/statistics');
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get overdue todos
ipcMain.handle('get-overdue-todos', async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/todos/overdue');
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get upcoming todos
ipcMain.handle('get-upcoming-todos', async () => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/todos/upcoming');
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});