"""
Persistent Storage Module

This module provides a robust, thread-safe persistent storage system for the application.
It implements a file-based storage mechanism with the following features:
- Thread-safe operations using locks
- In-memory caching for improved performance
- JSON-based file storage for data persistence
- Automatic storage directory management
- Global storage instance management

Key Components:
- PersistentStorage: Main storage class implementing thread-safe operations
- Global storage instance management functions
- Automatic storage directory creation and initialization
- Error handling for file operations

Dependencies:
    - json: For data serialization/deserialization
    - threading: For thread-safe operations
    - os: For file and directory operations
    - typing: For type hints
"""

import json
import os
import threading
from typing import Any, Dict, Optional

class PersistentStorage:
    """A thread-safe persistent storage implementation.
    
    This class provides a robust storage system with the following features:
    - Thread-safe read/write operations
    - In-memory caching with file persistence
    - Automatic storage directory management
    - JSON-based data serialization
    
    Attributes:
        _storage_file (str): Path to the JSON storage file
        _lock (threading.Lock): Thread synchronization lock
        _cache (Dict[str, Any]): In-memory cache of stored values
    """
    
    def __init__(self, storage_path: str):
        """Initialize the storage with the given file path.
        
        Args:
            storage_path: Path to the storage directory
            
        Note:
            Creates the storage directory and file if they don't exist
        """
        self._storage_file = os.path.join(storage_path, 'persistent_data.json')
        self._lock = threading.Lock()
        self._cache: Dict[str, Any] = {}
        self._ensure_storage_exists()
        self._load_data()
    
    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory and file exist."""
        os.makedirs(os.path.dirname(self._storage_file), exist_ok=True)
        if not os.path.exists(self._storage_file):
            with open(self._storage_file, 'w') as f:
                json.dump({}, f)
    
    def _load_data(self) -> None:
        """Load data from the storage file into memory."""
        with self._lock:
            try:
                with open(self._storage_file, 'r') as f:
                    self._cache = json.load(f)
            except json.JSONDecodeError:
                self._cache = {}
    
    def _save_data(self) -> None:
        """Save the current cache to the storage file."""
        # Prepare data while not holding the lock
        data_to_save = None
        with self._lock:
            data_to_save = self._cache.copy()
        
        # Write to file without holding the lock
        if data_to_save is not None:
            with open(self._storage_file, 'w') as f:
                json.dump(data_to_save, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from storage.
        
        Args:
            key: The key to retrieve
            default: Value to return if key doesn't exist
            
        Returns:
            The stored value or the default
        """
        with self._lock:
            return self._cache.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Store a value in storage.
        
        Args:
            key: The key to store the value under
            value: The value to store
        """
        with self._lock:
            self._cache[key] = value
        # Save data after releasing the lock
        self._save_data()
    
    def delete(self, key: str) -> None:
        """Delete a value from storage.
        
        Args:
            key: The key to delete
        """
        with self._lock:
            self._cache.pop(key, None)
        # Save data after releasing the lock
        self._save_data()
    
    def clear(self) -> None:
        """Clear all stored values."""
        with self._lock:
            self._cache.clear()
        # Save data after releasing the lock
        self._save_data()

# Create a global instance
_storage: Optional[PersistentStorage] = None

def init_storage(storage_path: str) -> None:
    """Initialize the global storage instance.
    
    Args:
        storage_path: Path to the storage directory
    """
    global _storage
    if _storage is None:
        _storage = PersistentStorage(storage_path)

def get_storage() -> PersistentStorage:
    """Get the global storage instance.
    
    Returns:
        The global PersistentStorage instance
        
    Raises:
        RuntimeError: If storage hasn't been initialized
    """
    if _storage is None:
        raise RuntimeError("Storage not initialized. Call init_storage first.")
    return _storage 