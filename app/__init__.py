"""Flask application factory."""
import logging
import os
from flask import Flask
from flask_migrate import Migrate

from app.config import Config
from app.extensions import db, login_manager
from app.models import User


def create_app(config_class=Config) -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id: str):
        """Load user by ID for Flask-Login."""
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.publisher import bp as publisher_bp
    app.register_blueprint(publisher_bp, url_prefix='/publisher')
    
    from app.advertiser import bp as advertiser_bp
    app.register_blueprint(advertiser_bp, url_prefix='/advertiser')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    # Bootstrap admin user if configured
    with app.app_context():
        db.create_all()
        _bootstrap_admin_user(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    
    return app


def _bootstrap_admin_user(app: Flask) -> None:
    """Create admin user from environment variables if configured."""
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    if not admin_email or not admin_password:
        return
    
    # Check if admin user already exists
    existing_admin = User.query.filter_by(email=admin_email, role='ADMIN').first()
    if existing_admin:
        return
    
    # Create admin user
    admin_user = User(
        email=admin_email,
        role='ADMIN'
    )
    admin_user.set_password(admin_password)
    
    try:
        db.session.add(admin_user)
        db.session.commit()
        app.logger.info(f'Admin user created: {admin_email}')
    except Exception as e:
        app.logger.error(f'Failed to create admin user: {e}')
        db.session.rollback()

