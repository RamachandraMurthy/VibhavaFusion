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
    
    This will start the development server on port 8080,
    accessible from any network interface.

Note:
    This is a development server configuration.
    For production deployment, use a production-grade WSGI server.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode, accessible from any network interface
    app.run(debug=True, host='0.0.0.0', port=8080) 