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

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.avatar import Avatar
from app.models.conversation import Conversation, Message
from app.services.ai_service import ai_service
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
    
    try:
        # Add user message
        user_message = Message(
            conversation_id=conversation_id,
            content=message_content,
            is_user=True
        )
        db.session.add(user_message)
        
        # Prepare conversation history for context
        recent_messages = conversation.get_recent_messages(5)  # Get last 5 messages
        messages = []
        
        # Add system message with avatar personality
        avatar = conversation.avatar
        system_message = {
            'role': 'system',
            'content': f"You are {avatar.name}, {avatar.personality}. Respond in character."
        }
        messages.append(system_message)
        
        # Add conversation history
        for msg in reversed(recent_messages):
            role = 'user' if msg.is_user else 'assistant'
            messages.append({
                'role': role,
                'content': msg.content
            })
        
        # Add current message
        messages.append({
            'role': 'user',
            'content': message_content
        })
        
        # Get AI response
        response = ai_service.generate_chat_response(
            messages,
            context=conversation.context
        )
        
        # Extract and save AI response
        ai_message_content = response['choices'][0]['message']['content']
        ai_message = Message(
            conversation_id=conversation_id,
            content=ai_message_content,
            is_user=False,
            message_data={
                'tokens': response.get('usage', {}).get('total_tokens', 0),
                'model': response.get('model', '')
            }
        )
        db.session.add(ai_message)
        
        # Update conversation timestamp
        conversation.last_message_at = ai_message.created_at
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'success',
                'message': ai_message.to_dict()
            })
            
    except Exception as e:
        db.session.rollback()
        error_msg = f"Error processing message: {str(e)}"
        flash(error_msg, 'error')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'status': 'error',
                'message': error_msg
            }), 500
    
    return redirect(url_for('conversation.view', conversation_id=conversation_id)) 