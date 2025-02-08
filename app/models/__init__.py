"""
Models Package

This package contains all database models for the application.
Models are defined using SQLAlchemy ORM and follow the Active Record pattern.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

def init_app(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    
    # Import models here to avoid circular imports
    from .user import User
    from .avatar import Avatar
    from .conversation import Conversation, Message
    
    # Create tables
    with app.app_context():
        db.create_all() 