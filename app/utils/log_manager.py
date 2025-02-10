"""
Log Manager Utility

This module provides centralized log management functionality for the application.
It handles log collection, filtering, and persistence.
"""

import logging
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class LogEntry:
    """Represents a single log entry"""
    timestamp: datetime
    level: str
    message: str
    details: Optional[Dict] = None

class LogManager:
    """Manages application logging and log retrieval"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure logging
        self.logger = logging.getLogger('app')
        self.logger.setLevel(logging.INFO)
        
        # File handler for all logs
        log_file = self.log_dir / "app.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def get_logs(self, 
                level: Optional[str] = None, 
                start_date: Optional[datetime] = None,
                end_date: Optional[datetime] = None,
                limit: int = 100) -> List[LogEntry]:
        """Retrieve logs with optional filtering"""
        logs = []
        log_file = self.log_dir / "app.log"
        
        if not log_file.exists():
            return []
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    # Parse log line
                    timestamp_str, level_str, message = line.split(' - ', 2)
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    
                    # Apply filters
                    if level and level.upper() != level_str:
                        continue
                    if start_date and timestamp < start_date:
                        continue
                    if end_date and timestamp > end_date:
                        continue
                    
                    logs.append(LogEntry(
                        timestamp=timestamp,
                        level=level_str,
                        message=message.strip()
                    ))
                except Exception:
                    continue
        
        # Return most recent logs first
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def clear_logs(self) -> bool:
        """Clear all logs"""
        try:
            log_file = self.log_dir / "app.log"
            if log_file.exists():
                log_file.unlink()
                log_file.touch()
            return True
        except Exception:
            return False
    
    def export_logs(self, 
                   level: Optional[str] = None,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> str:
        """Export logs as JSON"""
        logs = self.get_logs(level, start_date, end_date, limit=1000)
        return json.dumps([asdict(log) for log in logs], default=str)

# Initialize global log manager
log_manager = LogManager() 