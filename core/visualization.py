import matplotlib.pyplot as plt
import io
import base64
from core import tasks
from datetime import datetime, timedelta

def create_charts():
    """Create simple charts for tasks"""
    charts = {}
    all_tasks = tasks.list_tasks()
    
    if not all_tasks:
        return charts
    
    charts['status'] = status_chart(all_tasks)
    charts['due_dates'] = due_date_chart(all_tasks) 
    charts['trend'] = completion_trend(all_tasks)
    
    return charts

def status_chart(tasks_list):
    """Pie chart of task status"""
    status_count = {'pending': 0, 'completed': 0}
    
    for task in tasks_list:
        status = task[3] or 'pending'
        status_count[status] = status_count.get(status, 0) + 1
    
    plt.figure(figsize=(5, 3))
    plt.pie(status_count.values(), labels=status_count.keys(), autopct='%1.0f%%')
    plt.title('Task Status')
    
    return figure_to_image()

def due_date_chart(tasks_list):  # FIXED: Changed all_tasks to tasks_list
    """Bar chart of due dates"""
    today = datetime.now().date()
    counts = {'Overdue': 0, 'This Week': 0, 'Later': 0, 'No Date': 0}
    
    for task in tasks_list:  # FIXED: Changed all_tasks to tasks_list
        due_date = task[4]
        
        if not due_date:
            counts['No Date'] += 1
        elif due_date < today:
            counts['Overdue'] += 1
        elif (due_date - today).days <= 7:
            counts['This Week'] += 1
        else:
            counts['Later'] += 1
    
    plt.figure(figsize=(6, 4))
    plt.bar(counts.keys(), counts.values(), color=['red', 'orange', 'green', 'gray'])
    plt.title('Due Dates')
    plt.xticks(rotation=45)
    
    return figure_to_image()

def completion_trend(tasks_list):
    """Line chart of recent completions"""
    dates = []
    completions = []
    
    for days_ago in range(6, -1, -1):
        date = datetime.now().date() - timedelta(days=days_ago)
        dates.append(date.strftime('%m/%d'))
        
        # Count completions for this date
        count = 0
        for task in tasks_list:
            if task[3] == 'completed' and task[5] and task[5].date() == date:
                count += 1
        completions.append(count)
    
    plt.figure(figsize=(6, 4))
    plt.plot(dates, completions, marker='o')
    plt.title('Completed Tasks')
    plt.grid(True, alpha=0.3)
    
    return figure_to_image()

def figure_to_image():
    """Convert plot to base64 image"""
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode()
    plt.close()
    return img