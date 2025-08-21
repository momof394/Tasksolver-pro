#!/usr/bin/env python3
"""
Basic usage example for Tasksolver-pro.

This example demonstrates how to use the basic task management functionality.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from core.task_manager import TaskManager
from utils.helpers import Logger, format_timestamp


def main():
    """Main example function."""
    # Set up logging
    logger = Logger("BasicExample")
    logger.info("Starting Tasksolver-pro basic example")
    
    # Create a task manager
    task_manager = TaskManager()
    logger.info("Created task manager")
    
    # Create some example tasks
    tasks_to_create = [
        ("Set up development environment", "Install dependencies and configure workspace", "high"),
        ("Write project documentation", "Create user guides and API docs", "medium"),
        ("Implement user authentication", "Add login and registration functionality", "high"),
        ("Design user interface", "Create mockups and wireframes", "medium"),
        ("Set up testing framework", "Configure unit and integration tests", "low")
    ]
    
    logger.info(f"Creating {len(tasks_to_create)} example tasks")
    
    created_tasks = []
    for title, description, priority in tasks_to_create:
        task = task_manager.create_task(title, description, priority)
        created_tasks.append(task)
        logger.info(f"Created task: {task.title}")
    
    # Assign some tasks
    logger.info("Assigning tasks to team members")
    created_tasks[0].assign("developer1")
    created_tasks[1].assign("technical_writer")
    created_tasks[2].assign("developer2")
    created_tasks[3].assign("designer")
    created_tasks[4].assign("qa_engineer")
    
    # Complete a task
    created_tasks[0].complete()
    logger.info(f"Completed task: {created_tasks[0].title}")
    
    # Display task summary
    print("\n" + "="*50)
    print("TASK SUMMARY")
    print("="*50)
    
    pending_tasks = task_manager.get_tasks_by_status("pending")
    assigned_tasks = task_manager.get_tasks_by_status("assigned")
    completed_tasks = task_manager.get_tasks_by_status("completed")
    
    print(f"Total tasks: {len(task_manager.tasks)}")
    print(f"Pending: {len(pending_tasks)}")
    print(f"Assigned: {len(assigned_tasks)}")
    print(f"Completed: {len(completed_tasks)}")
    
    print("\nASSIGNED TASKS:")
    for task in assigned_tasks:
        print(f"  • {task.title} (assigned to: {task.assigned_to}, priority: {task.priority})")
    
    print("\nCOMPLETED TASKS:")
    for task in completed_tasks:
        print(f"  ✓ {task.title}")
    
    logger.info("Example completed successfully!")


if __name__ == "__main__":
    main()