"""Database models."""
from datetime import datetime
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.extensions import db


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # PUBLISHER, ADVERTISER, ADMIN
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    publisher_profile = db.relationship(
        'PublisherProfile',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    advertiser_profile = db.relationship(
        'AdvertiserProfile',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password: str) -> None:
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self) -> str:
        return f'<User {self.email}>'


class PublisherProfile(db.Model):
    """Publisher profile model."""
    __tablename__ = 'publisher_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f'<PublisherProfile {self.display_name}>'


class AdvertiserProfile(db.Model):
    """Advertiser profile model."""
    __tablename__ = 'advertiser_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f'<AdvertiserProfile {self.company_name}>'

