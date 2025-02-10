"""
Error Handlers Blueprint

This module contains error handlers for various HTTP error codes.
It provides consistent error pages and logging across the application.
"""

from flask import Blueprint, render_template
from app.utils.log_manager import log_manager

bp = Blueprint('errors', __name__)

@bp.app_errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    log_manager.logger.error(f"404 error: {error}")
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    log_manager.logger.error(f"500 error: {error}")
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors"""
    log_manager.logger.error(f"403 error: {error}")
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized errors"""
    log_manager.logger.error(f"401 error: {error}")
    return render_template('errors/401.html'), 401 