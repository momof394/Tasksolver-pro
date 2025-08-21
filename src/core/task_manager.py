"""
Core Task Management Module

This module contains the core functionality for task management
in the Tasksolver-pro application.
"""

class Task:
    """
    Represents a single task in the system.
    """
    
    def __init__(self, title, description="", priority="medium"):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "pending"
        self.assigned_to = None
        self.created_at = None
        self.updated_at = None
    
    def assign(self, user):
        """Assign the task to a user."""
        self.assigned_to = user
        self.status = "assigned"
    
    def complete(self):
        """Mark the task as completed."""
        self.status = "completed"
    
    def __repr__(self):
        return f"Task('{self.title}', status='{self.status}')"


class TaskManager:
    """
    Manages a collection of tasks.
    """
    
    def __init__(self):
        self.tasks = []
    
    def create_task(self, title, description="", priority="medium"):
        """Create a new task."""
        task = Task(title, description, priority)
        self.tasks.append(task)
        return task
    
    def get_tasks_by_status(self, status):
        """Get all tasks with a specific status."""
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_user(self, user):
        """Get all tasks assigned to a specific user."""
        return [task for task in self.tasks if task.assigned_to == user]