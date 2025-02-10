"""
Admin Blueprint - Handles all administrative routes and functionalities
This module contains all admin-related routes and access control decorators.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from functools import wraps
from flask_login import current_user, login_required

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
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """User management interface"""
    return render_template('admin/users.html')

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
    return render_template('admin/logs.html') 