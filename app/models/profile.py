"""
User Profile Model for VibhavaFusion.
Handles additional user information and preferences.
"""

from datetime import datetime
from app import db
from app.models.user import User

class Profile(db.Model):
    """User Profile model containing additional user information."""
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    avatar_url = db.Column(db.String(200))
    preferences = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with User model
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

    def __init__(self, user_id, **kwargs):
        """Initialize profile with user_id and optional fields."""
        super(Profile, self).__init__(user_id=user_id, **kwargs)
        if 'preferences' not in kwargs:
            self.preferences = {
                'email_notifications': True,
                'theme': 'light',
                'language': 'en'
            }

    def update(self, **kwargs):
        """Update profile fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convert profile to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'avatar_url': self.avatar_url,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def create_profile(user_id, **kwargs):
        """Create a new profile for a user."""
        profile = Profile(user_id=user_id, **kwargs)
        db.session.add(profile)
        db.session.commit()
        return profile 