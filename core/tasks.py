import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import get_connection
from core.merge_sort import sort_tasks

def run_query(query, params=(), fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall()
        else:
            result = cur.fetchone() if 'RETURNING' in query else None
        
        conn.commit()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def add_task(title, description=None, due_date=None):
    """Add a new task"""
    result = run_query(
        "INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s) RETURNING id",
        (title, description, due_date, 'pending')
    )
    
    if result:
        print(f"Task added with ID: {result[0]}")
        return result[0]
    return None

def list_tasks(status=None, sort_by='due_date', ascending=True):
    """Get all tasks with optional filtering and sorting"""
    query = "SELECT id, title, description, status, due_date, created_at FROM tasks"
    params = ()
    
    if status:
        query += " WHERE status = %s"
        params = (status,)
    
    tasks = run_query(query, params, fetch=True) or []
    sorted_tasks = sort_tasks(tasks, sort_by=sort_by, ascending=ascending)
    
    print(f"Found {len(sorted_tasks)} tasks")
    return sorted_tasks

def get_task(task_id):
    """Get a single task by ID"""
    task = run_query(
        "SELECT id, title, description, status, due_date, created_at FROM tasks WHERE id = %s",
        (task_id,),
        fetch=True
    )
    
    if task:
        print(f"Retrieved task {task_id}")
        return task[0]  # Return first result
    else:
        print(f"Task {task_id} not found")
        return None

def update_task(task_id, **updates):
    """Update task fields"""
    if not updates:
        print("No fields to update")
        return False
    
    # Build update query dynamically
    set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
    params = list(updates.values()) + [task_id]
    
    success = run_query(
        f"UPDATE tasks SET {set_clause} WHERE id = %s",
        params
    )
    
    if success is not None:
        print(f"Task {task_id} updated")
        return True
    return False

def delete_task(task_id):
    """Delete a task"""
    success = run_query("DELETE FROM tasks WHERE id = %s", (task_id,))
    
    if success is not None:
        print(f"Task {task_id} deleted")
        return True
    print(f"Task {task_id} not found")
    return False

def get_pending_tasks():
    """Get all pending tasks"""
    return list_tasks(status='pending')

def get_completed_tasks():
    """Get all completed tasks"""
    return list_tasks(status='completed')

def search_tasks(keyword):
    """Search tasks by keyword"""
    query = """
        SELECT id, title, description, status, due_date, created_at 
        FROM tasks 
        WHERE title ILIKE %s OR description ILIKE %s
    """
    
    tasks = run_query(query, (f"%{keyword}%", f"%{keyword}%"), fetch=True) or []
    print(f"Found {len(tasks)} tasks matching '{keyword}'")
    return tasks

# Test the module
if __name__ == "__main__":
    from db.database import init_db
    
    print("Testing tasks module...")
    init_db()
    
    # Simple test cases
    task_id = add_task("Simple Test Task", "Test description", "2024-12-31")
    
    if task_id:
        get_task(task_id)
        update_task(task_id, status='completed')
        search_tasks("test")
        delete_task(task_id)
    
    print("Test completed!")