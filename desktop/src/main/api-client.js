/**
 * API Client for backend communication.
 * Follows Single Responsibility Principle - handles HTTP requests.
 * Follows Dependency Inversion - can be easily mocked for testing.
 */
const { ipcRenderer } = require('electron');

class APIClient {
  /**
   * Generic IPC call handler.
   * Follows KISS Principle - simple, focused method.
   */
  async invoke(channel, ...args) {
    try {
      const result = await ipcRenderer.invoke(channel, ...args);
      if (!result.success) {
        throw new Error(result.error || 'API call failed');
      }
      return result.data;
    } catch (error) {
      console.error(`API Error [${channel}]:`, error);
      throw error;
    }
  }

  /**
   * Todo operations
   */
  async getTodos(filters = {}) {
    return this.invoke('get-todos', filters);
  }

  async createTodo(todoData) {
    return this.invoke('create-todo', todoData);
  }

  async updateTodo(id, todoData) {
    return this.invoke('update-todo', id, todoData);
  }

  async deleteTodo(id) {
    return this.invoke('delete-todo', id);
  }

  /**
   * Category operations
   */
  async getCategories() {
    return this.invoke('get-categories');
  }

  async createCategory(categoryData) {
    return this.invoke('create-category', categoryData);
  }

  async updateCategory(id, categoryData) {
    return this.invoke('update-category', id, categoryData);
  }

  async deleteCategory(id) {
    return this.invoke('delete-category', id);
  }

  /**
   * Statistics and special queries
   */
  async getStatistics() {
    return this.invoke('get-statistics');
  }

  async getOverdueTodos() {
    return this.invoke('get-overdue-todos');
  }

  async getUpcomingTodos() {
    return this.invoke('get-upcoming-todos');
  }
}

// Export singleton instance
module.exports = new APIClient();