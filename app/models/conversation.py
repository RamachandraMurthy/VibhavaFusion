"""
Conversation Models

This module defines the Conversation and Message models for managing chat interactions
between users and their AI avatars.
"""

from datetime import datetime
import json
from app import db
from app.models.user import User
from app.models.avatar import Avatar

class Conversation(db.Model):
    """A conversation between a user and their AI avatar."""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatars.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    context = db.Column(db.JSON)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('conversations', lazy='dynamic'))
    avatar = db.relationship('Avatar', backref=db.backref('conversations', lazy='dynamic'))
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, user_id, avatar_id, title, context=None):
        self.user_id = user_id
        self.avatar_id = avatar_id
        self.title = title
        self.context = context or {}
    
    def add_message(self, content, is_user=True, message_data=None):
        """Add a new message to the conversation."""
        message = Message(
            conversation_id=self.id,
            content=content,
            is_user=is_user,
            message_data=message_data
        )
        db.session.add(message)
        self.last_message_at = datetime.utcnow()
        return message
    
    def get_recent_messages(self, limit=10):
        """Get the most recent messages in the conversation."""
        return self.messages.order_by(Message.created_at.desc()).limit(limit).all()
    
    def set_context(self, key, value):
        """Update a specific context value."""
        if self.context is None:
            self.context = {}
        self.context[key] = value
    
    def get_context(self, key, default=None):
        """Get a specific context value."""
        return self.context.get(key, default) if self.context else default
    
    def to_dict(self):
        """Convert the conversation to a dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'avatar_id': self.avatar_id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'last_message_at': self.last_message_at.isoformat(),
            'is_active': self.is_active,
            'context': self.context
        }

class Message(db.Model):
    """A message within a conversation."""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_user = db.Column(db.Boolean, default=True)
    message_data = db.Column(db.JSON)
    
    def __init__(self, conversation_id, content, is_user=True, message_data=None):
        self.conversation_id = conversation_id
        self.content = content
        self.is_user = is_user
        self.message_data = message_data or {}
    
    def set_data(self, key, value):
        """Update a specific metadata value."""
        if self.message_data is None:
            self.message_data = {}
        self.message_data[key] = value
    
    def get_data(self, key, default=None):
        """Get a specific metadata value."""
        return self.message_data.get(key, default) if self.message_data else default
    
    def to_dict(self):
        """Convert the message to a dictionary."""
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'is_user': self.is_user,
            'message_data': self.message_data
        }
    
    def __repr__(self):
        return f'<Message {self.id} ({"User" if self.is_user else "Avatar"})>' 