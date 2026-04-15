const { contextBridge, ipcRenderer } = require('electron');

// API to expose to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Notifications
  showNotification: (title, body) => ipcRenderer.send('show-notification', { title, body }),
  
  // App info
  platform: process.platform,
  
  // Backend URL
  getBackendUrl: () => 'http://localhost:8000',
});

console.log('Preload script loaded');
