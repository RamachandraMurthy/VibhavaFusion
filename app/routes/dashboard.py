"""
Dashboard Routes

This module handles the user dashboard functionality, providing a central hub for:
- Overview of user's AI avatars
- Recent conversations
- Activity statistics
- Quick actions

Dependencies:
    - Flask: Core framework and routing
    - Flask-Login: User authentication
    - Models: Avatar and Conversation models
"""

from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from app.models.avatar import Avatar
from app.models.conversation import Conversation
from app.models.profile import Profile

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    """Display the user's dashboard with their avatars and recent activity."""
    # Get user's avatars
    avatars = Avatar.query.filter_by(user_id=current_user.id).all()
    
    # Get recent conversations
    recent_conversations = Conversation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Conversation.last_message_at.desc()
    ).limit(5).all()
    
    # Get user profile
    profile = current_user.profile or Profile.create_profile(current_user.id)
    
    return render_template(
        'dashboard/index.html',
        avatars=avatars,
        recent_conversations=recent_conversations,
        profile=profile
    ) 