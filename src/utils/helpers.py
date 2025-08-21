"""
Utility functions for the Tasksolver-pro application.
"""

import datetime
import hashlib


def generate_id(text):
    """Generate a unique ID from text input."""
    return hashlib.md5(text.encode()).hexdigest()[:8]


def format_timestamp(timestamp=None):
    """Format a timestamp for display."""
    if timestamp is None:
        timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def validate_priority(priority):
    """Validate that priority is a valid option."""
    valid_priorities = ["low", "medium", "high", "urgent"]
    return priority.lower() in valid_priorities


def sanitize_input(text):
    """Basic input sanitization."""
    if not isinstance(text, str):
        return str(text)
    return text.strip()


class Logger:
    """Simple logging utility."""
    
    def __init__(self, name):
        self.name = name
    
    def info(self, message):
        timestamp = format_timestamp()
        print(f"[{timestamp}] INFO [{self.name}]: {message}")
    
    def error(self, message):
        timestamp = format_timestamp()
        print(f"[{timestamp}] ERROR [{self.name}]: {message}")
    
    def debug(self, message):
        timestamp = format_timestamp()
        print(f"[{timestamp}] DEBUG [{self.name}]: {message}")