"""
Authentication Package

This package handles user authentication, registration, and session management.
It includes forms, routes, and utilities for user authentication.
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes, forms 