"""
Avatar Model

This module defines the Avatar model for managing AI personalities and their characteristics.
Each user can have multiple avatars with different personalities and learning histories.
"""

from datetime import datetime
import json
from app import db
from app.models.user import User

class Avatar(db.Model):
    """Avatar model for managing AI personalities."""
    
    __tablename__ = 'avatars'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    personality = db.Column(db.Text, nullable=False)  # JSON string of personality traits
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_interaction = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    learning_preferences = db.Column(db.Text)  # JSON string of learning preferences
    interaction_count = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('avatars', lazy='dynamic'))
    
    def __init__(self, user_id, name, personality_traits):
        self.user_id = user_id
        self.name = name
        self.set_personality(personality_traits)
    
    def set_personality(self, traits):
        """Set the avatar's personality traits."""
        self.personality = json.dumps(traits)
    
    def get_personality(self):
        """Get the avatar's personality traits."""
        return json.loads(self.personality)
    
    def update_learning_preferences(self, preferences):
        """Update the avatar's learning preferences."""
        self.learning_preferences = json.dumps(preferences)
        db.session.commit()
    
    def get_learning_preferences(self):
        """Get the avatar's learning preferences."""
        return json.loads(self.learning_preferences) if self.learning_preferences else {}
    
    def record_interaction(self):
        """Record an interaction with the avatar."""
        self.last_interaction = datetime.utcnow()
        self.interaction_count += 1
        db.session.commit()
    
    def to_dict(self):
        """Convert avatar object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'personality': self.get_personality(),
            'created_at': self.created_at.isoformat(),
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None,
            'is_active': self.is_active,
            'learning_preferences': self.get_learning_preferences(),
            'interaction_count': self.interaction_count
        }
    
    def __repr__(self):
        return f'<Avatar {self.name} (User: {self.user_id})>' 