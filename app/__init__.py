"""
Main Application Module

This module serves as the core initialization point for the Flask application.
It handles all the necessary setup including:
- Application factory pattern implementation
- Configuration loading and environment setup
- Blueprint registration for modular routing
- Error handler registration
- Logging configuration
- Database initialization
- Authentication setup

Dependencies:
    - Flask: Web framework
    - Flask-Login: For user authentication
    - Flask-SQLAlchemy: For database operations
    - Flask-Bcrypt: For password hashing
    - Flask-Migrate: For database migrations
"""

from flask import Flask, request, render_template
import logging
import os
from datetime import datetime
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

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

@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database."""
    from app.models.user import User
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import models
    from app.models.user import User
    from app.models.profile import Profile
    
    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.routes.avatar import bp as avatar_bp
    app.register_blueprint(avatar_bp, url_prefix='/avatar')
    
    from app.routes.profile import profile_bp as profile_bp
    app.register_blueprint(profile_bp)
    
    from app.routes.conversation import conversation_bp
    app.register_blueprint(conversation_bp, url_prefix='/conversation')
    
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Register error handlers
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
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
    
    @app.after_request
    def log_response_info(response):
        logger.info(f"Response status: {response.status}")
        return response
    
    @app.route('/test')
    def test():
        """A simple test route to verify the application is working."""
        return "Flask application is running!"
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# Import models after db is defined
from app.models import user, avatar, conversation 