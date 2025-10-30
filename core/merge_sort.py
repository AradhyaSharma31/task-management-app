def sort_tasks(tasks, sort_by='due_date', ascending=True):
    if len(tasks) <= 1:
        return tasks
    
    # Split
    mid = len(tasks) // 2
    left = sort_tasks(tasks[:mid], sort_by, ascending)
    right = sort_tasks(tasks[mid:], sort_by, ascending)
    
    # Merge
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Get values to compare
        a = get_value(left[i], sort_by)
        b = get_value(right[j], sort_by)
        
        # Handle None values (put them at the end)
        if a is None:
            take_left = not ascending
        elif b is None:
            take_left = ascending
        else:
            if ascending:
                take_left = a <= b
            else:
                take_left = a >= b
        
        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add leftovers
    return result + left[i:] + right[j:]

def get_value(task, field):
    """Get the value from task tuple based on field name"""
    # Task: (id, title, description, status, due_date, created_at)
    field_index = {
        'id': 0,
        'title': 1, 
        'status': 3,
        'due_date': 4,
        'created_at': 5
    }
    
    value = task[field_index[field]]
    
    # Make title lowercase for case-insensitive sorting
    if field == 'title' and value:
        return value.lower()
    
    return value