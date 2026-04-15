import React, { useState, useEffect, useCallback } from 'react';
import { Plus, Settings } from 'lucide-react';
import TodoList from './components/TodoList';
import TodoForm from './components/TodoForm';
import CategoryManager from './components/CategoryManager';
import SearchFilter from './components/SearchFilter';
import { todoApi, categoryApi, showNotification } from '../shared/api-client';

const PRIORITIES = [
  { value: 'urgent', label: 'Urgent', color: '#ef4444' },
  { value: 'high', label: 'High', color: '#f97316' },
  { value: 'medium', label: 'Medium', color: '#eab308' },
  { value: 'low', label: 'Low', color: '#22c55e' },
];

function App() {
  const [todos, setTodos] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [showCategories, setShowCategories] = useState(false);
  const [editingTodo, setEditingTodo] = useState(null);
  const [filters, setFilters] = useState({
    completed: '',
    priority: '',
    category_id: '',
    search: '',
    due_before: '',
  });

  // Fetch todos with filters
  const fetchTodos = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await todoApi.getTodos(filters);
      setTodos(data);
    } catch (err) {
      setError(err.message);
      console.error('Failed to fetch todos:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Fetch categories
  const fetchCategories = useCallback(async () => {
    try {
      const data = await categoryApi.getCategories();
      setCategories(data);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
    }
  }, []);

  // Initial load
  useEffect(() => {
    fetchTodos();
    fetchCategories();
  }, [fetchTodos, fetchCategories]);

  // Check for reminders
  useEffect(() => {
    const checkReminders = () => {
      const now = new Date();
      todos.forEach(todo => {
        if (todo.reminder_at && !todo.completed) {
          const reminderTime = new Date(todo.reminder_at);
          const timeDiff = Math.abs(now - reminderTime);
          if (timeDiff < 60000) { // Within 1 minute
            showNotification(
              'Todo Reminder',
              `Don't forget: ${todo.title}`
            );
          }
        }
      });
    };

    const interval = setInterval(checkReminders, 60000);
    return () => clearInterval(interval);
  }, [todos]);

  // Handle create
  const handleCreate = async (todoData) => {
    try {
      await todoApi.createTodo(todoData);
      fetchTodos();
      setShowForm(false);
      showNotification('Success', 'Todo created successfully');
    } catch (err) {
      setError(err.message);
    }
  };

  // Handle update
  const handleUpdate = async (todoData) => {
    try {
      await todoApi.updateTodo(editingTodo.id, todoData);
      fetchTodos();
      setShowForm(false);
      setEditingTodo(null);
      showNotification('Success', 'Todo updated successfully');
    } catch (err) {
      setError(err.message);
    }
  };

  // Handle delete
  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) return;
    try {
      await todoApi.deleteTodo(id);
      fetchTodos();
      showNotification('Success', 'Todo deleted successfully');
    } catch (err) {
      setError(err.message);
    }
  };

  // Handle toggle complete
  const handleToggleComplete = async (id, completed) => {
    try {
      await todoApi.toggleComplete(id, completed);
      fetchTodos();
    } catch (err) {
      setError(err.message);
    }
  };

  // Handle edit click
  const handleEdit = (todo) => {
    setEditingTodo(todo);
    setShowForm(true);
  };

  // Handle filter change
  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  // Handle category created
  const handleCategoryCreated = () => {
    fetchCategories();
  };

  // Calculate stats
  const stats = {
    total: todos.length,
    completed: todos.filter(t => t.completed).length,
    pending: todos.filter(t => !t.completed).length,
    overdue: todos.filter(t => {
      if (t.completed || !t.due_date) return false;
      return new Date(t.due_date) < new Date();
    }).length,
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-title">
            <h1>📋 TodoList</h1>
            <div className="stats">
              <span className="stat">
                <span className="stat-value">{stats.total}</span>
                <span className="stat-label">Total</span>
              </span>
              <span className="stat">
                <span className="stat-value">{stats.pending}</span>
                <span className="stat-label">Pending</span>
              </span>
              <span className="stat">
                <span className="stat-value">{stats.completed}</span>
                <span className="stat-label">Done</span>
              </span>
              {stats.overdue > 0 && (
                <span className="stat overdue">
                  <span className="stat-value">{stats.overdue}</span>
                  <span className="stat-label">Overdue</span>
                </span>
              )}
            </div>
          </div>
          <div className="header-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setShowCategories(true)}
            >
              <Settings size={18} />
              Categories
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => {
                setEditingTodo(null);
                setShowForm(true);
              }}
            >
              <Plus size={18} />
              New Todo
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main">
        <SearchFilter
          filters={filters}
          onFilterChange={handleFilterChange}
          categories={categories}
          priorities={PRIORITIES}
        />

        {error && (
          <div className="error-banner">
            {error}
            <button type="button" onClick={() => setError(null)}>×</button>
          </div>
        )}

        <TodoList
          todos={todos}
          loading={loading}
          categories={categories}
          priorities={PRIORITIES}
          onToggleComplete={handleToggleComplete}
          onEdit={handleEdit}
          onDelete={handleDelete}
        />
      </main>

      {/* Todo Form Modal */}
      {showForm && (
        <TodoForm
          todo={editingTodo}
          categories={categories}
          priorities={PRIORITIES}
          onSubmit={editingTodo ? handleUpdate : handleCreate}
          onCancel={() => {
            setShowForm(false);
            setEditingTodo(null);
          }}
        />
      )}

      {/* Category Manager Modal */}
      {showCategories && (
        <CategoryManager
          categories={categories}
          onCategoryCreated={handleCategoryCreated}
          onCategoryDeleted={fetchCategories}
          onClose={() => setShowCategories(false)}
        />
      )}
    </div>
  );
}

export default App;
