"""
Unit tests for the Task Management module.
"""

import unittest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from core.task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """Test the Task class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.task = Task("Test Task", "Test description", "high")
    
    def test_task_creation(self):
        """Test that tasks are created correctly."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test description")
        self.assertEqual(self.task.priority, "high")
        self.assertEqual(self.task.status, "pending")
        self.assertIsNone(self.task.assigned_to)
    
    def test_task_assignment(self):
        """Test task assignment functionality."""
        self.task.assign("john_doe")
        self.assertEqual(self.task.assigned_to, "john_doe")
        self.assertEqual(self.task.status, "assigned")
    
    def test_task_completion(self):
        """Test task completion functionality."""
        self.task.complete()
        self.assertEqual(self.task.status, "completed")


class TestTaskManager(unittest.TestCase):
    """Test the TaskManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = TaskManager()
    
    def test_task_creation(self):
        """Test creating tasks through the manager."""
        task = self.manager.create_task("New Task", "Description", "low")
        self.assertIn(task, self.manager.tasks)
        self.assertEqual(task.title, "New Task")
    
    def test_get_tasks_by_status(self):
        """Test filtering tasks by status."""
        task1 = self.manager.create_task("Task 1")
        task2 = self.manager.create_task("Task 2")
        task1.complete()
        
        pending_tasks = self.manager.get_tasks_by_status("pending")
        completed_tasks = self.manager.get_tasks_by_status("completed")
        
        self.assertIn(task2, pending_tasks)
        self.assertIn(task1, completed_tasks)
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
    
    def test_get_tasks_by_user(self):
        """Test filtering tasks by assigned user."""
        task1 = self.manager.create_task("Task 1")
        task2 = self.manager.create_task("Task 2")
        task1.assign("user1")
        task2.assign("user2")
        
        user1_tasks = self.manager.get_tasks_by_user("user1")
        user2_tasks = self.manager.get_tasks_by_user("user2")
        
        self.assertIn(task1, user1_tasks)
        self.assertIn(task2, user2_tasks)
        self.assertEqual(len(user1_tasks), 1)
        self.assertEqual(len(user2_tasks), 1)


if __name__ == '__main__':
    unittest.main()