"""
Avatar Routes

This module handles avatar creation, customization, and interaction.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.avatar import Avatar
from app.models.conversation import Conversation

bp = Blueprint('avatar', __name__, url_prefix='/avatar')

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        personality = {
            'traits': request.form.getlist('traits'),
            'interests': request.form.getlist('interests'),
            'communication_style': request.form.get('communication_style'),
            'knowledge_focus': request.form.getlist('knowledge_focus')
        }
        
        avatar = Avatar(
            user_id=current_user.id,
            name=name,
            personality_traits=personality
        )
        
        db.session.add(avatar)
        db.session.commit()
        
        flash(f'Avatar {name} created successfully!', 'success')
        return redirect(url_for('avatar.customize', avatar_id=avatar.id))
    
    return render_template('avatar/create.html')

@bp.route('/<int:avatar_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(avatar_id):
    avatar = Avatar.query.get_or_404(avatar_id)
    
    if avatar.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        personality = {
            'traits': request.form.getlist('traits'),
            'interests': request.form.getlist('interests'),
            'communication_style': request.form.get('communication_style'),
            'knowledge_focus': request.form.getlist('knowledge_focus')
        }
        
        avatar.name = name
        avatar.personality_traits = personality
        db.session.commit()
        
        flash(f'Avatar {name} updated successfully!', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('avatar/edit.html', avatar=avatar)

@bp.route('/<int:avatar_id>/customize', methods=['GET', 'POST'])
@login_required
def customize(avatar_id):
    avatar = Avatar.query.get_or_404(avatar_id)
    
    if avatar.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        personality = avatar.get_personality()
        personality.update({
            'learning_style': request.form.get('learning_style'),
            'response_length': request.form.get('response_length'),
            'formality_level': request.form.get('formality_level')
        })
        
        avatar.set_personality(personality)
        avatar.update_learning_preferences({
            'preferred_topics': request.form.getlist('preferred_topics'),
            'interaction_frequency': request.form.get('interaction_frequency'),
            'feedback_style': request.form.get('feedback_style')
        })
        
        db.session.commit()
        flash('Avatar preferences updated successfully!', 'success')
        return redirect(url_for('avatar.chat', avatar_id=avatar.id))
    
    return render_template('avatar/customize.html', avatar=avatar)

@bp.route('/<int:avatar_id>/chat', methods=['GET', 'POST'])
@login_required
def chat(avatar_id):
    avatar = Avatar.query.get_or_404(avatar_id)
    
    if avatar.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    
    # Get or create active conversation
    conversation = Conversation.query.filter_by(
        user_id=current_user.id,
        avatar_id=avatar_id,
        is_active=True
    ).first()
    
    if not conversation:
        conversation = Conversation(
            user_id=current_user.id,
            avatar_id=avatar_id,
            title=f"Chat with {avatar.name}"
        )
        db.session.add(conversation)
        db.session.commit()
    
    return render_template('avatar/chat.html', avatar=avatar, conversation=conversation)

@bp.route('/<int:avatar_id>/message', methods=['POST'])
@login_required
def send_message(avatar_id):
    avatar = Avatar.query.get_or_404(avatar_id)
    
    if avatar.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    message = data.get('message')
    conversation_id = data.get('conversation_id')
    
    conversation = Conversation.query.get_or_404(conversation_id)
    
    # Add user message
    conversation.add_message(message, is_user=True)
    
    # TODO: Process message with OpenAI and get response
    # This will be implemented in the next phase
    
    return jsonify({'status': 'Message sent'}) 