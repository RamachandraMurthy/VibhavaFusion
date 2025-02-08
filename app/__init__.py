"""
Main Application Module

This module serves as the core initialization point for the Flask application.
It handles all the necessary setup including:
- Application factory pattern implementation
- Configuration loading and environment setup
- Blueprint registration for modular routing
- Error handler registration
- Logging configuration
- Persistent storage initialization
- Template context processors for global template variables

Dependencies:
    - Flask: Web framework
    - logging: For application-wide logging
    - datetime: For template context processing
    - config.config: Application configuration management
    - storage.persistent: Persistent data storage system
"""

from flask import Flask, request, render_template
import logging
import os
from datetime import datetime
from config.config import get_config
from storage.persistent import init_storage

# Configure logging with detailed format for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def not_found_error(error):
    """Handle 404 Not Found errors.
    
    Args:
        error: The error instance from Flask
        
    Returns:
        tuple: Rendered 404 template and status code
    """
    logger.error(f"404 error: {error}")
    return render_template('404.html'), 404

def internal_error(error):
    """Handle 500 Internal Server errors.
    
    Args:
        error: The error instance from Flask
        
    Returns:
        tuple: Rendered 500 template and status code
    """
    logger.error(f"500 error: {error}")
    return render_template('500.html'), 500

def create_app():
    """Create and configure the Flask application.
    
    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config())
    
    # Ensure storage directory exists
    storage_path = app.config['PERSISTENT_STORAGE_PATH']
    logger.debug(f"Storage path: {storage_path}")
    try:
        os.makedirs(storage_path, exist_ok=True)
        logger.debug("Storage directory created/verified")
    except Exception as dir_error:
        logger.error(f"Failed to create storage directory: {dir_error}")
        raise
    
    try:
        # Initialize persistent storage
        logger.debug("Before storage initialization")
        init_storage(storage_path)
        logger.debug("After storage initialization")
        logger.info("Storage initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize storage: {e}", exc_info=True)
        raise
    
    try:
        # Register blueprints
        from app.routes.main import main_bp
        app.register_blueprint(main_bp)
        logger.info("Blueprints registered successfully")
    except Exception as e:
        logger.error(f"Failed to register blueprints: {e}")
    
    try:
        # Register error handlers
        app.register_error_handler(404, not_found_error)
        app.register_error_handler(500, internal_error)
        logger.info("Error handlers registered successfully")
    except Exception as e:
        logger.error(f"Failed to register error handlers: {e}")
    
    # Add template context processors
    @app.context_processor
    def utility_processor():
        return {
            'now': datetime.now
        }
    
    # Add request logging
    @app.before_request
    def log_request_info():
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug('Headers: %s', request.headers)
        logger.debug('Body: %s', request.get_data())
    
    @app.after_request
    def log_response_info(response):
        logger.info(f"Response status: {response.status}")
        return response
    
    @app.route('/test')
    def test():
        """A simple test route to verify the application is working."""
        return "Flask application is running!"
    
    return app 