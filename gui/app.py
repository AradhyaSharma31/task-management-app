import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry

from core import tasks
from utils.helper import format_date, safe_strftime
from db.database import init_db

class TaskManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize database first
        self.initialize_database()
        
        # Sorting options
        self.current_sort = 'due_date'
        self.ascending = True
        
        self.title("📝 Task Management System")
        self.geometry("900x550")
        self.configure(bg="#f4f4f4")
        self.create_widgets()
        self.refresh_tasks()

    def initialize_database(self):
        """Initialize the database and ensure table exists"""
        try:
            init_db()
        except Exception as e:
            messagebox.showerror("Database Error", 
                                f"Failed to initialize database:\n{e}\n\n"
                                "Please check your database connection and credentials.")
            self.destroy()
            return

    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self, bg="#f4f4f4")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame: Add task
        add_frame = tk.Frame(main_container, bg="#f4f4f4")
        add_frame.pack(fill=tk.X, pady=10)

        # Title
        tk.Label(add_frame, text="Title:*", bg="#f4f4f4", fg="red").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.title_var = tk.StringVar()
        title_entry = tk.Entry(add_frame, textvariable=self.title_var, width=25)
        title_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        title_entry.focus()

        # Description
        tk.Label(add_frame, text="Description:", bg="#f4f4f4").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.desc_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=self.desc_var, width=25).grid(row=0, column=3, padx=5, pady=2, sticky="w")

        # Due Date with Date Picker
        tk.Label(add_frame, text="Due Date:", bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        
        self.due_date_entry = DateEntry(
            add_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            mindate=None,
        )
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Add Task Button
        tk.Button(add_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white").grid(row=1, column=2, padx=5, pady=2, sticky="w")

        # Sorting controls frame
        sort_frame = tk.Frame(main_container, bg="#f4f4f4")
        sort_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(sort_frame, text="Sort by:", bg="#f4f4f4").pack(side=tk.LEFT, padx=5)
        
        # Sort field dropdown
        self.sort_var = tk.StringVar(value="due_date")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var, width=12, state="readonly")
        sort_combo['values'] = ('due_date', 'created_at', 'title', 'status', 'id')
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind('<<ComboboxSelected>>', self.on_sort_change)
        
        # Sort order button
        self.sort_order_btn = tk.Button(sort_frame, text="↑ Ascending", command=self.toggle_sort_order)
        self.sort_order_btn.pack(side=tk.LEFT, padx=5)
        
        # Control buttons frame
        control_frame = tk.Frame(main_container, bg="#f4f4f4")
        control_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(control_frame, text="🔄 Refresh", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="✅ Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🗑️ Delete Selected", command=self.delete_selected, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)

        # Treeview: Task list
        tree_frame = tk.Frame(main_container)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Description", "Status", "Due", "Created"), show="headings")
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due", text="Due Date")
        self.tree.heading("Created", text="Created At")

        self.tree.column("ID", width=40)
        self.tree.column("Title", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Status", width=80)
        self.tree.column("Due", width=100)
        self.tree.column("Created", width=120)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind double-click to edit task
        self.tree.bind("<Double-1>", self.on_task_double_click)

    def on_sort_change(self, event=None):
        """Handle sort field change"""
        self.current_sort = self.sort_var.get()
        self.refresh_tasks()

    def toggle_sort_order(self):
        """Toggle between ascending and descending order"""
        self.ascending = not self.ascending
        self.sort_order_btn.config(text="↑ Ascending" if self.ascending else "↓ Descending")
        self.refresh_tasks()

    def add_task(self):
        title = self.title_var.get().strip()
        description = self.desc_var.get().strip()
        
        # Get date from DateEntry widget
        due_date = self.due_date_entry.get_date()

        if not title:
            messagebox.showwarning("Input Error", "Task title is required.")
            return
        
        task_id = tasks.add_task(title, description, due_date)
        if task_id:
            self.title_var.set("")
            self.desc_var.set("")
            # Reset date to today
            self.due_date_entry.set_date(None)
            self.refresh_tasks()
            messagebox.showinfo("Success", f"Task added successfully with ID: {task_id}")
        else:
            messagebox.showerror("Error", "Failed to add task. Please check the console for details.")

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
            return
        
        success_count = 0
        for item in selected:
            task_id = self.tree.item(item)['values'][0]
            if tasks.update_task(task_id, status='completed'):
                success_count += 1
        
        if success_count > 0:
            self.refresh_tasks()
            messagebox.showinfo("Success", f"Marked {success_count} task(s) as complete.")
        else:
            messagebox.showerror("Error", "Failed to update tasks.")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {len(selected)} selected task(s)?"):
            success_count = 0
            for item in selected:
                task_id = self.tree.item(item)['values'][0]
                if tasks.delete_task(task_id):
                    success_count += 1
            
            if success_count > 0:
                self.refresh_tasks()
                messagebox.showinfo("Success", f"Deleted {success_count} task(s).")
            else:
                messagebox.showerror("Error", "Failed to delete tasks.")

    def on_task_double_click(self, event):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            values = self.tree.item(item)['values']
            self.edit_task(values[0])

    def edit_task(self, task_id):
        current_title = ""
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == task_id:
                current_title = self.tree.item(item)['values'][1]
                break
        
        new_title = simpledialog.askstring("Edit Task", "Enter new title:", initialvalue=current_title)
        if new_title and new_title.strip():
            if tasks.update_task(task_id, title=new_title.strip()):
                self.refresh_tasks()
            else:
                messagebox.showerror("Error", "Failed to update task.")

    def refresh_tasks(self):
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Get tasks with current sorting options
            all_tasks = tasks.list_tasks(sort_by=self.current_sort, ascending=self.ascending)
            if not all_tasks:
                # Insert a placeholder for empty list
                self.tree.insert("", "end", values=("", "No tasks found", "", "", "", ""))
                return
                
            for task in all_tasks:
                task_id, title, desc, status, due_date, created_at = task
                
                # Handle None values
                status = status or "pending"
                description = desc or ""
                
                # Format dates safely
                due_str = safe_strftime(due_date, "%Y-%m-%d")
                created_str = safe_strftime(created_at, "%Y-%m-%d %H:%M")
                
                self.tree.insert("", "end", values=(task_id, title, description, status, due_str, created_str))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh tasks: {e}")


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()