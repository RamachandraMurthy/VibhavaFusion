import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    APP_NAME = 'VibhavaFusion'
    
    # Flask-Login Configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    SESSION_PROTECTION = 'strong'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Storage Configuration
    STORAGE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'storage')
    DATA_PATH = os.path.join(STORAGE_PATH, 'data')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Vector Database Configuration
    VECTOR_DB_PATH = os.path.join(STORAGE_PATH, 'vector_db')
    
    # Development Configuration
    DEBUG = True
    TESTING = False
    
    # Static Files
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # Security Configuration
    BCRYPT_LOG_ROUNDS = 12
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration."""
        # Ensure storage directories exist
        os.makedirs(Config.DATA_PATH, exist_ok=True)
        os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    def __init__(self):
        super().__init__()
        # Only enforce these checks when actually running in production
        if os.environ.get('FLASK_ENV') == 'production':
            if not self.SECRET_KEY or self.SECRET_KEY == 'dev-key-please-change-in-production':
                raise ValueError('No SECRET_KEY set for production configuration')
            if not self.SQLALCHEMY_DATABASE_URI or 'sqlite' in self.SQLALCHEMY_DATABASE_URI:
                raise ValueError('Production should not use SQLite database')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 