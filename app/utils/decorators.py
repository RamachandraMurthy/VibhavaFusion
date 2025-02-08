"""
Utility Decorators

This module provides custom decorators for route protection and validation.
"""

from functools import wraps
from flask import abort
from flask_login import current_user

def verify_user(f):
    """Decorator to verify that the current user has access to the requested resource."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function 