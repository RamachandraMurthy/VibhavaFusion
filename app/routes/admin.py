"""
Admin Blueprint - Handles all administrative routes and functionalities
This module contains all admin-related routes and access control decorators.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from functools import wraps
from flask_login import current_user, login_required
from app.models.user import User
from app import db
from datetime import datetime, timedelta
from app.utils.log_manager import log_manager

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this area.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard showing overview of system statistics and quick actions"""
    # Get user statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    
    # Get today's events (placeholder for now)
    events_today = 0
    
    # Get pending tasks (placeholder for now)
    pending_tasks = 0
    
    # Get recent activities (placeholder for now)
    recent_activities = []
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         active_users=active_users,
                         events_today=events_today,
                         pending_tasks=pending_tasks,
                         recent_activities=recent_activities)

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """User management interface"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/settings')
@login_required
@admin_required
def admin_settings():
    """System settings and configuration interface"""
    return render_template('admin/settings.html')

@admin_bp.route('/logs')
@login_required
@admin_required
def view_logs():
    """System logs and activity monitoring"""
    level = request.args.get('level', None)
    date_str = request.args.get('date', None)
    
    # Parse date filter if provided
    start_date = None
    if date_str:
        try:
            start_date = datetime.strptime(date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)
        except ValueError:
            start_date = end_date = None
    
    # Get filtered logs
    logs = log_manager.get_logs(
        level=level,
        start_date=start_date,
        end_date=end_date if start_date else None
    )
    
    return render_template('admin/logs.html', logs=logs)

@admin_bp.route('/logs/download')
@login_required
@admin_required
def download_logs():
    """Download logs as JSON"""
    level = request.args.get('level', None)
    date_str = request.args.get('date', None)
    
    # Parse date filter if provided
    start_date = None
    if date_str:
        try:
            start_date = datetime.strptime(date_str, '%Y-%m-%d')
            end_date = start_date + timedelta(days=1)
        except ValueError:
            start_date = end_date = None
    
    # Export logs
    logs_json = log_manager.export_logs(
        level=level,
        start_date=start_date,
        end_date=end_date if start_date else None
    )
    
    return jsonify({'logs': logs_json})

@admin_bp.route('/logs/clear', methods=['POST'])
@login_required
@admin_required
def clear_logs():
    """Clear all system logs"""
    success = log_manager.clear_logs()
    return jsonify({'success': success}) 