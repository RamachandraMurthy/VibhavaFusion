"""
Main Routes Blueprint

This module implements the main routes for the Flask application.
"""

from flask import Blueprint, render_template, current_app, redirect, url_for
import logging

# Configure route-specific logger
logger = logging.getLogger(__name__)

# Create the blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the application's index page."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}", exc_info=True)
        return render_template('errors/500.html'), 500

@bp.route('/create-avatar')
def create_avatar():
    """Redirect to avatar creation."""
    return redirect(url_for('avatar.create'))

@bp.route('/test-links')
def test_links():
    """Temporary route to display all available application links for testing."""
    try:
        return render_template('main/test_links.html')
    except Exception as e:
        logger.error(f"Error in test links route: {str(e)}", exc_info=True)
        return render_template('errors/500.html'), 500 