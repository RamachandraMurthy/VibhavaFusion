"""
Configuration Module

This module manages the application's configuration settings across different environments.
It provides a hierarchical configuration system with:
- Base configuration class with common settings
- Environment-specific configurations (development, testing, production)
- Secure loading of sensitive values from environment variables
- Easy access to configuration values through a factory function

Key Features:
- Environment-based configuration selection
- Secure secret key management
- Static and template folder configuration
- Application-wide settings management

Dependencies:
    - os: For environment variable and path handling
    - python-dotenv: For loading environment variables from .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file for secure configuration
load_dotenv()

class Config:
    """Base configuration class with common settings.
    
    This class defines the base configuration settings that are common across all
    environments. It serves as the parent class for environment-specific configs.
    
    Attributes:
        SECRET_KEY (str): Application secret key for security
        STATIC_FOLDER (str): Directory for static files
        TEMPLATES_FOLDER (str): Directory for HTML templates
        APP_NAME (str): Application name
        PERSISTENT_STORAGE_PATH (str): Path to data storage directory
    """
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Application settings
    APP_NAME = 'VibhavaFusion'
    PERSISTENT_STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'storage', 'data')

class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    ENV = 'development'

class TestingConfig(Config):
    """Testing environment configuration."""
    
    DEBUG = False
    TESTING = True
    ENV = 'testing'

class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    ENV = 'production'
    
    # Override the default secret key
    SECRET_KEY = os.getenv('SECRET_KEY')

# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get the current configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'default')
    return config[env] 