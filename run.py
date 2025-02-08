"""
Application Entry Point

This module serves as the main entry point for running the Flask application.
It provides:
- Application instance creation using the factory pattern
- Development server configuration
- Debug mode settings
- Network interface binding
- Port configuration

Usage:
    Run directly with Python:
    ```
    python run.py
    ```
    
    This will start the development server on port 5000,
    accessible from any network interface.

Note:
    This is a development server configuration.
    For production deployment, use a production-grade WSGI server.
"""

import os
from app import create_app
from config import config

# Get configuration based on environment
config_name = os.environ.get('FLASK_CONFIG', 'default')
app = create_app(config[config_name])

if __name__ == '__main__':
    # Run the application in debug mode, accessible from any network interface
    app.run(host='127.0.0.1', port=5000, debug=True) 