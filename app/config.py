"""Application configuration."""
import os
from typing import Optional


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('SECRET_KEY environment variable is required')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError('DATABASE_URL environment variable is required')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Flask settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    DEBUG = FLASK_ENV == 'development'
    
    # Server port
    PORT = int(os.environ.get('PORT', 8000))
    
    # Admin bootstrap (optional)
    ADMIN_EMAIL: Optional[str] = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD: Optional[str] = os.environ.get('ADMIN_PASSWORD')

