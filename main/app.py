import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from core import tasks
from db.database import init_db
from core.visualization import create_charts

app = Flask(__name__)
CORS(app)

# Start database
init_db()

def task_to_dict(task):
    """Convert task tuple to dictionary"""
    return {
        'id': task[0],
        'title': task[1],
        'description': task[2],
        'status': task[3],
        'due_date': str(task[4]) if task[4] else None,
        'created_at': str(task[5]) if task[5] else None
    }

@app.route('/')
def home():
    return jsonify({"message": "Task API", "status": "running"})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    status = request.args.get('status')
    sort_by = request.args.get('sort_by', 'due_date')
    ascending = request.args.get('ascending', 'true').lower() == 'true'
    
    tasks_list = tasks.list_tasks(status=status, sort_by=sort_by, ascending=ascending)
    tasks_dict = [task_to_dict(task) for task in tasks_list]
    
    return jsonify({'success': True, 'tasks': tasks_dict, 'count': len(tasks_dict)})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create new task"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'success': False, 'error': 'Title required'}), 400
    
    task_id = tasks.add_task(data['title'], data.get('description'), data.get('due_date'))
    
    if task_id:
        return jsonify({'success': True, 'task_id': task_id, 'message': 'Task created'})
    return jsonify({'success': False, 'error': 'Create failed'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get one task"""
    task = tasks.get_task(task_id)
    
    if task:
        return jsonify({'success': True, 'task': task_to_dict(task)})
    return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data'}), 400
    
    # Only update fields that are provided
    updates = {k: v for k, v in data.items() if k in ['title', 'description', 'status', 'due_date']}
    
    if tasks.update_task(task_id, **updates):
        return jsonify({'success': True, 'message': 'Task updated'})
    return jsonify({'success': False, 'error': 'Update failed'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task"""
    if tasks.delete_task(task_id):
        return jsonify({'success': True, 'message': 'Task deleted'})
    return jsonify({'success': False, 'error': 'Delete failed'}), 500

@app.route('/api/tasks/search')
def search_tasks():
    """Search tasks"""
    keyword = request.args.get('q')
    
    if not keyword:
        return jsonify({'success': False, 'error': 'Keyword required'}), 400
    
    results = tasks.search_tasks(keyword)
    tasks_dict = [task_to_dict(task) for task in results]
    
    return jsonify({'success': True, 'tasks': tasks_dict, 'count': len(tasks_dict)})

@app.route('/api/stats')
def get_stats():
    """Get task statistics"""
    all_tasks = tasks.list_tasks()
    
    total = len(all_tasks)
    pending = len([t for t in all_tasks if t[3] == 'pending'])
    completed = len([t for t in all_tasks if t[3] == 'completed'])
    
    from datetime import date
    today = date.today()
    overdue = len([t for t in all_tasks if t[3] == 'pending' and t[4] and t[4] < today])
    
    completion_rate = round((completed / total * 100), 2) if total > 0 else 0
    
    stats = {
        'total_tasks': total,
        'pending_tasks': pending,
        'completed_tasks': completed,
        'overdue_tasks': overdue,
        'completion_rate': completion_rate
    }
    
    return jsonify({'success': True, 'statistics': stats})

@app.route('/api/charts')
def get_charts():
    """Get all charts"""
    charts = create_charts()
    return jsonify({'success': True, 'charts': charts})

if __name__ == '__main__':
    app.run(debug=True, port=5000)