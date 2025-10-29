from datetime import datetime
from typing import List, Tuple

def merge_sort(tasks: List[Tuple], sort_by: str = 'due_date', ascending: bool = True) -> List[Tuple]:
    """
    Merge sort algorithm to sort tasks by various criteria.
    
    Args:
        tasks: List of task tuples (id, title, description, status, due_date, created_at)
        sort_by: Field to sort by ('due_date', 'created_at', 'title', 'status')
        ascending: True for ascending order, False for descending
    
    Returns:
        Sorted list of tasks
    """
    if len(tasks) <= 1:
        return tasks
    
    # Split the list into two halves
    mid = len(tasks) // 2
    left_half = tasks[:mid]
    right_half = tasks[mid:]
    
    # Recursively sort both halves
    left_sorted = merge_sort(left_half, sort_by, ascending)
    right_sorted = merge_sort(right_half, sort_by, ascending)
    
    # Merge the sorted halves
    return merge(left_sorted, right_sorted, sort_by, ascending)

def merge(left: List[Tuple], right: List[Tuple], sort_by: str, ascending: bool) -> List[Tuple]:
    """
    Merge two sorted lists into one sorted list.
    """
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        left_task = left[i]
        right_task = right[j]
        
        # Get comparison values based on sort_by field
        left_val = get_sort_value(left_task, sort_by)
        right_val = get_sort_value(right_task, sort_by)
        
        # Handle None values (tasks without due dates go to the end)
        if left_val is None:
            should_swap = not ascending
        elif right_val is None:
            should_swap = ascending
        else:
            if ascending:
                should_swap = left_val <= right_val
            else:
                should_swap = left_val >= right_val
        
        if should_swap:
            merged.append(left_task)
            i += 1
        else:
            merged.append(right_task)
            j += 1
    
    # Add remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged

def get_sort_value(task: Tuple, sort_by: str):
    """
    Extract the sort value from a task tuple based on the field name.
    
    Task tuple structure: (id, title, description, status, due_date, created_at)
    """
    if sort_by == 'due_date':
        return task[4]  # due_date is at index 4
    elif sort_by == 'created_at':
        return task[5]  # created_at is at index 5
    elif sort_by == 'title':
        return task[1].lower()  # title at index 1, convert to lowercase for case-insensitive sort
    elif sort_by == 'status':
        return task[3]  # status at index 3
    elif sort_by == 'id':
        return task[0]  # id at index 0
    else:
        raise ValueError(f"Invalid sort field: {sort_by}")

def sort_tasks(tasks: List[Tuple], sort_by: str = 'due_date', ascending: bool = True) -> List[Tuple]:
    """
    Wrapper function to sort tasks using merge sort.
    
    Args:
        tasks: List of task tuples
        sort_by: Field to sort by
        ascending: Sort order
    
    Returns:
        Sorted list of tasks
    """
    if not tasks:
        return []
    
    return merge_sort(tasks, sort_by, ascending)