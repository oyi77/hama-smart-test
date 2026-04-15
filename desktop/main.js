const { app } = require('electron');
const { createMainWindow, setupNotificationHandler } = require('./src/main/window');

function initializeApp() {
  // Setup IPC handlers
  setupNotificationHandler();

  // Create main window
  createMainWindow();

  // macOS: Re-create window when dock icon clicked
  app.on('activate', () => {
    const { getMainWindow } = require('./src/main/window');
    if (getMainWindow() === null) {
      createMainWindow();
    }
  });
}

// App ready
app.whenReady().then(initializeApp);

// Quit when all windows closed (except macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
