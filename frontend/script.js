const API = 'http://localhost:5000/api';
let currentTasks = [];
let currentSection = 'dashboard';

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    setupEventListeners();
});

function setupEventListeners() {
    // Search with debounce
    document.getElementById('search-input').addEventListener('input', debounce(searchTasks, 300));
    
    // Task form
    document.getElementById('task-form').addEventListener('submit', handleTaskSubmit);
    
    // Close modal on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeTaskModal();
    });
}

// Navigation
function showSection(section) {
    currentSection = section;
    
    // Update active nav
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelector(`.nav-item:nth-child(${section === 'dashboard' ? 1 : section === 'tasks' ? 2 : 3})`).classList.add('active');
    
    // Update page title
    const titles = {
        dashboard: 'Dashboard',
        tasks: 'All Tasks',
        analytics: 'Analytics'
    };
    
    const subtitles = {
        dashboard: 'Manage your tasks efficiently',
        tasks: 'View and manage all your tasks',
        analytics: 'Detailed insights and analytics'
    };
    
    document.getElementById('page-title').textContent = titles[section];
    document.getElementById('page-subtitle').textContent = subtitles[section];
    
    // Show/hide sections
    document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
    document.getElementById(section).classList.add('active');
    
    // Load section data
    if (section === 'dashboard') loadDashboard();
    else if (section === 'tasks') loadTasks();
    else if (section === 'analytics') loadAnalytics();
}

// Dashboard
async function loadDashboard() {
    await loadStatistics();
    await loadRecentTasks();
    await loadCharts();
    await loadQuickStats();
}

// Load tasks
async function loadTasks(status = null) {
    showLoading('#tasks-container');
    
    try {
        let url = `${API}/tasks`;
        const params = new URLSearchParams();
        
        if (status) params.append('status', status);
        params.append('sort_by', document.getElementById('sort-by').value);
        params.append('ascending', document.getElementById('sort-order').value);
        
        if (params.toString()) url += '?' + params.toString();
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            currentTasks = data.tasks;
            displayTasks(data.tasks);
            updateBadges();
        } else {
            showToast('Failed to load tasks', 'error');
        }
    } catch (error) {
        showToast('Error loading tasks', 'error');
        showTasks([]);
    }
}

// Display tasks
function displayTasks(tasks) {
    const container = document.getElementById('tasks-container');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = `
            <div class="empty">
                <i class="fas fa-tasks"></i>
                <h3>No tasks found</h3>
                <p>Get started by creating your first task!</p>
                <button class="btn btn-primary" onclick="openTaskModal()" style="margin-top: 1rem;">
                    <i class="fas fa-plus"></i> Create Task
                </button>
            </div>
        `;
        return;
    }
    
    const today = new Date().toISOString().split('T')[0];
    
    container.innerHTML = tasks.map(task => `
        <div class="task-item ${task.status === 'completed' ? 'completed' : ''} ${task.due_date && task.due_date < today && task.status !== 'completed' ? 'overdue' : ''}">
            <div class="task-content">
                <div class="task-title">${escapeHtml(task.title)}</div>
                ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
                <div class="task-meta">
                    ${task.due_date ? `<span><i class="fas fa-calendar"></i> Due: ${formatDate(task.due_date)}</span>` : ''}
                    <span><i class="fas fa-clock"></i> Created: ${formatDate(task.created_at)}</span>
                    <span><i class="fas fa-circle" style="color: ${task.status === 'completed' ? '#10b981' : '#f59e0b'}"></i> ${task.status}</span>
                </div>
            </div>
            <div class="task-actions">
                ${task.status !== 'completed' ? 
                    `<button class="task-btn btn-complete" onclick="markComplete(${task.id})" title="Complete">
                        <i class="fas fa-check"></i>
                    </button>` : ''}
                <button class="task-btn btn-edit" onclick="editTask(${task.id})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="task-btn btn-delete" onclick="deleteTask(${task.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Recent tasks
async function loadRecentTasks() {
    try {
        const response = await fetch(`${API}/tasks?sort_by=created_at&ascending=false`);
        const data = await response.json();
        
        if (data.success) {
            displayRecentTasks(data.tasks.slice(0, 5));
        }
    } catch (error) {
        console.error('Error loading recent tasks:', error);
    }
}

function displayRecentTasks(tasks) {
    const container = document.getElementById('recent-tasks-container');
    
    if (!tasks || tasks.length === 0) {
        container.innerHTML = '<p style="color: var(--text-light); text-align: center;">No tasks yet</p>';
        return;
    }
    
    container.innerHTML = tasks.map(task => `
        <div class="task-item" style="margin-bottom: 1rem; padding: 1rem;">
            <div class="task-content">
                <div class="task-title" style="font-size: 1rem;">${escapeHtml(task.title)}</div>
                <div class="task-meta" style="font-size: 0.75rem;">
                    ${task.due_date ? `Due: ${formatDate(task.due_date)} • ` : ''}
                    Status: <strong style="color: ${task.status === 'completed' ? '#10b981' : '#f59e0b'}">${task.status}</strong>
                </div>
            </div>
        </div>
    `).join('');
}

// Quick stats
async function loadQuickStats() {
    try {
        const response = await fetch(`${API}/tasks`);
        const data = await response.json();
        
        if (data.success) {
            const tasks = data.tasks;
            const today = new Date().toISOString().split('T')[0];
            const oneWeekLater = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
            
            const overdue = tasks.filter(t => t.due_date && t.due_date < today && t.status !== 'completed').length;
            const dueThisWeek = tasks.filter(t => t.due_date && t.due_date <= oneWeekLater && t.due_date >= today && t.status !== 'completed').length;
            const highPriority = tasks.filter(t => t.status !== 'completed').length; // Simple priority calculation
            
            document.getElementById('overdue-tasks').textContent = overdue;
            document.getElementById('due-this-week').textContent = dueThisWeek;
            document.getElementById('high-priority').textContent = highPriority;
        }
    } catch (error) {
        console.error('Error loading quick stats:', error);
    }
}

// Statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API}/stats`);
        const data = await response.json();
        
        if (data.success) {
            const stats = data.statistics;
            
            document.getElementById('total-tasks').textContent = stats.total_tasks;
            document.getElementById('pending-tasks').textContent = stats.pending_tasks;
            document.getElementById('completed-tasks').textContent = stats.completed_tasks;
            document.getElementById('completion-rate').textContent = stats.completion_rate + '%';
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Analytics
async function loadAnalytics() {
    // Implement advanced analytics here
    showToast('Analytics loaded successfully!', 'success');
}

// Charts
async function loadCharts() {
    try {
        const response = await fetch(`${API}/charts`);
        const data = await response.json();
        
        if (data.success && data.charts) {
            displayCharts(data.charts);
        }
    } catch (error) {
        console.error('Error loading charts:', error);
    }
}

function displayCharts(charts) {
    const container = document.getElementById('charts-container');
    
    let html = '<div class="charts-grid">';
    
    if (charts.status) {
        html += `
            <div class="chart-card">
                <h4>Task Status Distribution</h4>
                <img src="data:image/png;base64,${charts.status}" alt="Status Chart">
            </div>
        `;
    }
    
    if (charts.due_dates) {
        html += `
            <div class="chart-card">
                <h4>Due Date Overview</h4>
                <img src="data:image/png;base64,${charts.due_dates}" alt="Due Dates Chart">
            </div>
        `;
    }
    
    if (charts.trend) {
        html += `
            <div class="chart-card">
                <h4>Completion Trend</h4>
                <img src="data:image/png;base64,${charts.trend}" alt="Trend Chart">
            </div>
        `;
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Task actions
async function markComplete(taskId) {
    try {
        const response = await fetch(`${API}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({status: 'completed'})
        });
        
        if (response.ok) {
            showToast('Task completed!', 'success');
            loadDashboard();
            if (currentSection === 'tasks') loadTasks();
        }
    } catch (error) {
        showToast('Error completing task', 'error');
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        const response = await fetch(`${API}/tasks/${taskId}`, {method: 'DELETE'});
        
        if (response.ok) {
            showToast('Task deleted!', 'success');
            loadDashboard();
            if (currentSection === 'tasks') loadTasks();
        }
    } catch (error) {
        showToast('Error deleting task', 'error');
    }
}

// Search
async function searchTasks() {
    const keyword = document.getElementById('search-input').value.trim();
    
    if (!keyword) {
        loadTasks();
        return;
    }
    
    showLoading('#tasks-container');
    
    try {
        const response = await fetch(`${API}/tasks/search?q=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        if (data.success) {
            displayTasks(data.tasks);
        }
    } catch (error) {
        showToast('Search failed', 'error');
    }
}

// Modal functions
function openTaskModal(taskId = null) {
    const modal = document.getElementById('task-modal');
    
    if (taskId) {
        document.getElementById('modal-title').textContent = 'Edit Task';
        const task = currentTasks.find(t => t.id === taskId);
        if (task) {
            document.getElementById('task-id').value = task.id;
            document.getElementById('task-title').value = task.title;
            document.getElementById('task-description').value = task.description || '';
            document.getElementById('task-due-date').value = task.due_date || '';
        }
    } else {
        document.getElementById('modal-title').textContent = 'Add New Task';
        document.getElementById('task-form').reset();
        document.getElementById('task-id').value = '';
    }
    
    modal.style.display = 'block';
}

function closeTaskModal() {
    document.getElementById('task-modal').style.display = 'none';
}

async function handleTaskSubmit(event) {
    event.preventDefault();
    
    const taskId = document.getElementById('task-id').value;
    const title = document.getElementById('task-title').value.trim();
    
    if (!title) {
        showToast('Task title is required', 'error');
        return;
    }
    
    const taskData = {
        title: title,
        description: document.getElementById('task-description').value.trim() || null,
        due_date: document.getElementById('task-due-date').value || null
    };
    
    try {
        const url = taskId ? `${API}/tasks/${taskId}` : `${API}/tasks`;
        const method = taskId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(taskData)
        });
        
        if (response.ok) {
            showToast(taskId ? 'Task updated!' : 'Task created!', 'success');
            closeTaskModal();
            loadDashboard();
            if (currentSection === 'tasks') loadTasks();
        }
    } catch (error) {
        showToast('Error saving task', 'error');
    }
}

function editTask(taskId) {
    openTaskModal(taskId);
}

// Utility functions
function updateBadges() {
    const total = currentTasks.length;
    const pending = currentTasks.filter(t => t.status === 'pending').length;
    const completed = currentTasks.filter(t => t.status === 'completed').length;
    
    document.getElementById('total-tasks-badge').textContent = total;
    document.getElementById('pending-badge').textContent = pending;
    document.getElementById('completed-badge').textContent = completed;
}

function showLoading(selector) {
    const container = document.querySelector(selector);
    container.innerHTML = '<div class="loading">Loading...</div>';
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}"></i>
        ${message}
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function formatDate(dateString) {
    if (!dateString) return 'No date';
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Close modal when clicking outside
window.onclick = function(e) {
    const modal = document.getElementById('task-modal');
    if (e.target === modal) {
        closeTaskModal();
    }
}