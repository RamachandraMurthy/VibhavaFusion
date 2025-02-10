"""
Test Log Generator

This script generates sample logs for testing the admin logs interface.
It creates a variety of log entries with different levels and messages.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.log_manager import log_manager
from datetime import datetime, timedelta
import random
import time

# Sample log messages
INFO_MESSAGES = [
    "User logged in successfully",
    "Profile updated",
    "New conversation started",
    "Message sent successfully",
    "Avatar generated",
    "Settings updated",
    "Database backup completed",
    "Cache cleared",
    "Email notification sent",
    "File uploaded successfully"
]

WARNING_MESSAGES = [
    "High CPU usage detected",
    "Low disk space warning",
    "Failed login attempt",
    "Slow database query detected",
    "API rate limit approaching",
    "Memory usage above threshold",
    "Deprecated function called",
    "Session timeout",
    "Invalid file format uploaded",
    "Database connection pool near capacity"
]

ERROR_MESSAGES = [
    "Database connection failed",
    "API request failed",
    "File upload error",
    "Authentication failed",
    "Invalid configuration",
    "Memory limit exceeded",
    "Unhandled exception",
    "Network timeout",
    "Permission denied",
    "Resource not found"
]

DEBUG_MESSAGES = [
    "Starting background task",
    "Cache hit ratio: 85%",
    "Query execution time: 150ms",
    "Memory usage: 512MB",
    "Active connections: 25",
    "Processing queue items",
    "Initializing service",
    "Loading configuration",
    "Validating input",
    "Checking permissions"
]

def generate_logs(num_entries=100, days_back=7):
    """Generate sample log entries"""
    
    print(f"Generating {num_entries} log entries...")
    
    for _ in range(num_entries):
        # Random timestamp within the last week
        timestamp = datetime.now() - timedelta(
            days=random.uniform(0, days_back),
            hours=random.uniform(0, 24),
            minutes=random.uniform(0, 60)
        )
        
        # Random log level and message
        level = random.choice(['INFO', 'WARNING', 'ERROR', 'DEBUG'])
        if level == 'INFO':
            message = random.choice(INFO_MESSAGES)
        elif level == 'WARNING':
            message = random.choice(WARNING_MESSAGES)
        elif level == 'ERROR':
            message = random.choice(ERROR_MESSAGES)
        else:
            message = random.choice(DEBUG_MESSAGES)
        
        # Log the message
        getattr(log_manager.logger, level.lower())(message)
        
        # Small delay to avoid identical timestamps
        time.sleep(0.01)
    
    print("Log generation complete!")

if __name__ == '__main__':
    # Clear existing logs
    log_manager.clear_logs()
    
    # Generate new logs
    generate_logs() 