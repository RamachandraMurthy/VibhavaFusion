"""
Conversation Routes

This module handles the conversation functionality between users and their AI avatars.
It includes routes for:
- Starting new conversations
- Viewing conversation history
- Managing active conversations

Dependencies:
    - Flask: Core framework and routing
    - Flask-Login: User authentication
    - Models: Avatar and Conversation models
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.avatar import Avatar
from app.models.conversation import Conversation, Message
from app import db

conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/start/<int:avatar_id>')
@login_required
def start(avatar_id):
    """Start a new conversation with an avatar."""
    avatar = Avatar.query.get_or_404(avatar_id)
    
    if avatar.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    # Create new conversation
    conversation = Conversation(
        user_id=current_user.id,
        avatar_id=avatar_id,
        title=f"Chat with {avatar.name}"
    )
    db.session.add(conversation)
    db.session.commit()
    
    return redirect(url_for('conversation.view', conversation_id=conversation.id))

@conversation_bp.route('/view/<int:conversation_id>')
@login_required
def view(conversation_id):
    """View a specific conversation."""
    conversation = Conversation.query.get_or_404(conversation_id)
    
    if conversation.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template(
        'conversation/view.html',
        conversation=conversation,
        avatar=conversation.avatar
    )

@conversation_bp.route('/send/<int:conversation_id>', methods=['POST'])
@login_required
def send_message(conversation_id):
    """Send a message in a conversation."""
    conversation = Conversation.query.get_or_404(conversation_id)
    
    if conversation.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    message_content = request.form.get('message')
    if not message_content:
        flash('Message cannot be empty.', 'error')
        return redirect(url_for('conversation.view', conversation_id=conversation_id))
    
    # Add user message
    message = Message(
        conversation_id=conversation_id,
        content=message_content,
        is_user=True
    )
    db.session.add(message)
    
    # TODO: Generate AI response using OpenAI
    # For now, just echo back a simple response
    ai_response = Message(
        conversation_id=conversation_id,
        content=f"You said: {message_content}",
        is_user=False
    )
    db.session.add(ai_response)
    
    # Update conversation timestamp
    conversation.last_message_at = message.created_at
    db.session.commit()
    
    return redirect(url_for('conversation.view', conversation_id=conversation_id)) 