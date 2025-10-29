import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import get_connection
from core.merge_sort import sort_tasks

def add_task(title, description=None, due_date=None):
    """
    Add a new task to the database.
    
    Args:
        title (str): Task title (required)
        description (str, optional): Task description
        due_date (datetime.date, optional): Due date for the task
    
    Returns:
        int: Task ID if successful, None if failed
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, description, due_date, status) VALUES (%s, %s, %s, %s) RETURNING id",
            (title, description, due_date, 'pending')
        )
        task_id = cur.fetchone()[0]
        conn.commit()
        print(f"Task added with ID: {task_id}")
        return task_id
    except Exception as e:
        print(f"Error adding task: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def list_tasks(status=None, sort_by='due_date', ascending=True):
    """
    Retrieve tasks from the database with optional filtering and sorting.
    
    Args:
        status (str, optional): Filter by status ('pending', 'completed')
        sort_by (str): Field to sort by ('due_date', 'created_at', 'title', 'status', 'id')
        ascending (bool): Sort order (True for ascending, False for descending)
    
    Returns:
        list: List of task tuples (id, title, description, status, due_date, created_at)
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT id, title, description, status, due_date, created_at FROM tasks"
        params = ()
        if status:
            query += " WHERE status = %s"
            params = (status,)
        
        # Execute query without ORDER BY since we'll use our algorithm
        cur.execute(query, params)
        tasks_list = cur.fetchall()
        
        # Sort tasks using our merge sort algorithm
        sorted_tasks = sort_tasks(tasks_list, sort_by=sort_by, ascending=ascending)
        
        print(f"Retrieved {len(sorted_tasks)} tasks sorted by {sort_by} ({'ascending' if ascending else 'descending'})")
        return sorted_tasks
    except Exception as e:
        print(f"Error listing tasks: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_task(task_id):
    """
    Retrieve a single task by ID.
    
    Args:
        task_id (int): The ID of the task to retrieve
    
    Returns:
        tuple: Task tuple (id, title, description, status, due_date, created_at) or None if not found
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, title, description, status, due_date, created_at FROM tasks WHERE id = %s",
            (task_id,)
        )
        task = cur.fetchone()
        if task:
            print(f"Retrieved task {task_id}")
        else:
            print(f"Task {task_id} not found")
        return task
    except Exception as e:
        print(f"Error retrieving task {task_id}: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def update_task(task_id, title=None, description=None, status=None, due_date=None):
    """
    Update an existing task.
    
    Args:
        task_id (int): The ID of the task to update
        title (str, optional): New title
        description (str, optional): New description
        status (str, optional): New status ('pending', 'completed')
        due_date (datetime.date, optional): New due date
    
    Returns:
        bool: True if successful, False if failed
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        updates = []
        params = []
        
        # Build dynamic update query based on provided fields
        if title is not None:
            updates.append("title = %s")
            params.append(title)
        if description is not None:
            updates.append("description = %s")
            params.append(description)
        if status is not None:
            updates.append("status = %s")
            params.append(status)
        if due_date is not None:
            updates.append("due_date = %s")
            params.append(due_date)
            
        if not updates:
            print("No fields to update.")
            return False
            
        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
        cur.execute(query, params)
        conn.commit()
        print(f"Task {task_id} updated.")
        return True
    except Exception as e:
        print(f"Error updating task {task_id}: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_task(task_id):
    """
    Delete a task from the database.
    
    Args:
        task_id (int): The ID of the task to delete
    
    Returns:
        bool: True if successful, False if failed
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        rows_affected = cur.rowcount
        conn.commit()
        if rows_affected > 0:
            print(f"Task {task_id} deleted.")
            return True
        else:
            print(f"Task {task_id} not found.")
            return False
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_tasks_by_status(status):
    """
    Get all tasks with a specific status.
    
    Args:
        status (str): Status to filter by ('pending', 'completed')
    
    Returns:
        list: List of tasks with the specified status
    """
    return list_tasks(status=status)

def get_pending_tasks():
    """
    Get all pending tasks.
    
    Returns:
        list: List of pending tasks
    """
    return get_tasks_by_status('pending')

def get_completed_tasks():
    """
    Get all completed tasks.
    
    Returns:
        list: List of completed tasks
    """
    return get_tasks_by_status('completed')

def search_tasks(keyword, search_fields=['title', 'description']):
    """
    Search tasks by keyword in specified fields.
    
    Args:
        keyword (str): Search keyword
        search_fields (list): Fields to search in ['title', 'description']
    
    Returns:
        list: List of matching tasks
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Build search conditions
        conditions = []
        params = []
        for field in search_fields:
            if field in ['title', 'description']:
                conditions.append(f"{field} ILIKE %s")
                params.append(f"%{keyword}%")
        
        if not conditions:
            return []
            
        query = f"""
            SELECT id, title, description, status, due_date, created_at 
            FROM tasks 
            WHERE {' OR '.join(conditions)}
            ORDER BY created_at DESC
        """
        
        cur.execute(query, params)
        tasks_list = cur.fetchall()
        print(f"Found {len(tasks_list)} tasks matching '{keyword}'")
        return tasks_list
    except Exception as e:
        print(f"Error searching tasks: {e}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Test function when run directly
if __name__ == "__main__":
    # Test the module functions
    from db.database import init_db
    
    print("Testing tasks module...")
    
    # Initialize database
    init_db()
    
    # Test adding tasks
    print("\n1. Testing add_task...")
    task1_id = add_task("Test Task 1", "This is a test task", "2024-12-31")
    task2_id = add_task("Test Task 2", "Another test task", "2024-11-15")
    task3_id = add_task("Test Task 3 - No due date")
    
    # Test listing tasks
    print("\n2. Testing list_tasks...")
    all_tasks = list_tasks()
    print(f"Found {len(all_tasks)} tasks")
    
    # Test sorting
    print("\n3. Testing sorting...")
    tasks_by_title = list_tasks(sort_by='title', ascending=True)
    tasks_by_due_date = list_tasks(sort_by='due_date', ascending=False)
    
    # Test updating task
    print("\n4. Testing update_task...")
    if task1_id:
        update_task(task1_id, status='completed')
    
    # Test getting single task
    print("\n5. Testing get_task...")
    if task1_id:
        task = get_task(task1_id)
        print(f"Retrieved task: {task}")
    
    # Test search
    print("\n6. Testing search_tasks...")
    search_results = search_tasks("test")
    print(f"Search found {len(search_results)} tasks")
    
    # Test cleanup
    print("\n8. Testing delete_task...")
    if task1_id:
        delete_task(task1_id)
    if task2_id:
        delete_task(task2_id)
    if task3_id:
        delete_task(task3_id)
    
    print("\nAll tests completed!")