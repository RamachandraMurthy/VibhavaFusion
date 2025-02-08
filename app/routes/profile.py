"""
Profile management routes for VibhavaFusion.
Handles user profile creation, updates, and viewing.
"""

from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.profile import Profile
from app.utils.decorators import verify_user

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """Display the user's profile page."""
    profile = current_user.profile or Profile.create_profile(current_user.id)
    return render_template('profile/view.html', profile=profile)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Handle profile editing."""
    profile = current_user.profile or Profile.create_profile(current_user.id)
    
    if request.method == 'POST':
        try:
            profile.update(
                full_name=request.form.get('full_name'),
                bio=request.form.get('bio'),
                location=request.form.get('location'),
                website=request.form.get('website')
            )
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.view_profile'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'error')
    
    return render_template('profile/edit.html', profile=profile)

@profile_bp.route('/profile/preferences', methods=['GET', 'POST'])
@login_required
def manage_preferences():
    """Handle user preferences."""
    profile = current_user.profile or Profile.create_profile(current_user.id)
    
    if request.method == 'POST':
        try:
            preferences = {
                'email_notifications': request.form.get('email_notifications') == 'on',
                'theme': request.form.get('theme', 'light'),
                'language': request.form.get('language', 'en')
            }
            profile.update(preferences=preferences)
            flash('Preferences updated successfully!', 'success')
            return redirect(url_for('profile.view_profile'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating preferences. Please try again.', 'error')
    
    return render_template('profile/preferences.html', profile=profile)

@profile_bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile_api():
    """API endpoint to get user profile data."""
    profile = current_user.profile
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    return jsonify(profile.to_dict())

@profile_bp.route('/api/profile', methods=['PUT'])
@login_required
def update_profile_api():
    """API endpoint to update user profile data."""
    profile = current_user.profile
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    try:
        data = request.get_json()
        profile.update(**data)
        return jsonify(profile.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 