"""
Main Routes Blueprint

This module implements the main routes for the Flask application.
It demonstrates best practices for:
- Blueprint organization and structure
- Integration with persistent storage
- Flash messaging implementation
- Template rendering with context
- Error handling and logging
- Visit counting functionality

Key Features:
- Index route with visit counter
- Welcome and milestone messages
- Debug routes for testing
- Comprehensive error handling
- Detailed logging

Dependencies:
    - Flask: For routing and templating
    - logging: For route-specific logging
    - storage.persistent: For persistent visit counter
"""

from flask import Blueprint, render_template, flash, current_app, Response
import logging
from storage.persistent import get_storage
from typing import Union, Tuple

# Configure route-specific logger
logger = logging.getLogger(__name__)

# Create the blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index() -> Union[str, Tuple[str, int]]:
    """Render the application's index page.
    
    This route demonstrates several key features:
    1. Persistent storage usage for visit counting
    2. Flash messaging for user feedback
    3. Template inheritance and rendering
    4. Error handling with logging
    5. Type-safe return values
    
    Returns:
        Union[str, Tuple[str, int]]: 
            - On success: Rendered template string
            - On error: Tuple of error template and status code
    """
    try:
        logger.info("Starting index route processing")
        visit_count = 0  # Default value
        
        # Example of using persistent storage
        try:
            logger.debug("Before getting storage instance")
            storage = get_storage()
            logger.debug("After getting storage instance")
            
            # Get current count without updating storage yet
            logger.debug("Before getting visit count")
            current_count = storage.get('visit_count', 0)
            logger.debug(f"Current count retrieved: {current_count}")
            
            visit_count = current_count + 1
            logger.debug(f"New count calculated: {visit_count}")
            
            # Update storage in a separate try block
            try:
                logger.debug("Before setting new count")
                storage.set('visit_count', visit_count)
                logger.debug("After setting new count")
            except Exception as write_error:
                logger.error(f"Failed to update visit count: {write_error}", exc_info=True)
                # Continue with current count even if save fails
                visit_count = current_count
        except Exception as storage_error:
            logger.error(f"Storage error: {storage_error}", exc_info=True)
            logger.debug("Using default visit count of 0")
        
        logger.debug("Before flash messages")
        # Example of flash messaging
        if visit_count == 1:
            flash('Welcome to the application!', 'success')
        elif visit_count % 10 == 0:
            flash(f'Thanks for visiting {visit_count} times!', 'info')
        logger.debug("After flash messages")
        
        logger.debug("Before template rendering")
        template_vars = {
            'visit_count': visit_count,
            'config': current_app.config
        }
        logger.debug(f"Template variables prepared: {template_vars}")
        
        try:
            logger.debug("Attempting to render template")
            rendered = render_template('index.html', **template_vars)
            logger.debug("Template rendered successfully")
            return rendered
        except Exception as template_error:
            logger.error(f"Template error: {template_error}", exc_info=True)
            return render_template('500.html'), 500
                             
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}", exc_info=True)
        return render_template('500.html'), 500

@main_bp.route('/debug')
def debug() -> str:
    """A debug route to verify the application is working."""
    return "Flask blueprint is working!"

@main_bp.route('/debug-test')
def debug_test() -> str:
    """A simple debug route that returns plain text."""
    logger.info("Debug test route accessed")
    return "Debug route is working!" 