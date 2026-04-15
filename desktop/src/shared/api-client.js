import axios from 'axios';

// Get backend URL from electron or fallback to localhost
const getBaseURL = () => {
  if (window.electronAPI?.getBackendUrl) {
    return window.electronAPI.getBackendUrl();
  }
  return 'http://localhost:8000';
};

// Create axios instance
const apiClient = axios.create({
  baseURL: `${getBaseURL()}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Error handling interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
    console.error('API Error:', errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
);

// Todo API
export const todoApi = {
  // Get all todos with optional filters
  getTodos: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value);
      }
    });
    const response = await apiClient.get(`/todos?${params.toString()}`);
    return response.data;
  },

  // Get single todo
  getTodo: async (id) => {
    const response = await apiClient.get(`/todos/${id}`);
    return response.data;
  },

  // Create new todo
  createTodo: async (todoData) => {
    const response = await apiClient.post('/todos', todoData);
    return response.data;
  },

  // Update todo
  updateTodo: async (id, todoData) => {
    const response = await apiClient.put(`/todos/${id}`, todoData);
    return response.data;
  },

  // Delete todo
  deleteTodo: async (id) => {
    await apiClient.delete(`/todos/${id}`);
  },

  // Toggle todo completion
  toggleComplete: async (id, completed) => {
    const response = await apiClient.put(`/todos/${id}`, { completed });
    return response.data;
  },
};

// Category API
export const categoryApi = {
  // Get all categories
  getCategories: async () => {
    const response = await apiClient.get('/categories');
    return response.data;
  },

  // Create category
  createCategory: async (categoryData) => {
    const response = await apiClient.post('/categories', categoryData);
    return response.data;
  },

  // Update category
  updateCategory: async (id, categoryData) => {
    const response = await apiClient.put(`/categories/${id}`, categoryData);
    return response.data;
  },

  // Delete category
  deleteCategory: async (id) => {
    await apiClient.delete(`/categories/${id}`);
  },
};

// Notification helper
export const showNotification = (title, body) => {
  if (window.electronAPI?.showNotification) {
    window.electronAPI.showNotification(title, body);
  } else {
    // Fallback to browser notification
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, { body });
    }
  }
};

export default apiClient;
