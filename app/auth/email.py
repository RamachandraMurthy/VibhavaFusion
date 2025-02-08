"""
Email Authentication Module

This module handles all email-related authentication functionality including:
- Email verification for new registrations
- Password reset requests and confirmation
- Email notifications for security events

Dependencies:
    - Flask-Mail: For sending emails
    - JWT: For generating secure tokens
    - Templates: For email content rendering
"""

from flask import current_app, render_template
from flask_mail import Message
import jwt
from datetime import datetime, timedelta
from app import mail
from app.models.user import User

def send_email(subject, recipients, html_body, text_body):
    """Send an email using Flask-Mail."""
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=text_body,
        html=html_body
    )
    mail.send(msg)

def send_verification_email(user):
    """Send an email verification link to the user."""
    token = generate_verification_token(user)
    send_email(
        'Verify Your Email',
        [user.email],
        render_template('auth/email/verify_email.html', user=user, token=token),
        render_template('auth/email/verify_email.txt', user=user, token=token)
    )

def send_password_reset_email(user):
    """Send a password reset link to the user."""
    token = generate_reset_token(user)
    send_email(
        'Reset Your Password',
        [user.email],
        render_template('auth/email/reset_password.html', user=user, token=token),
        render_template('auth/email/reset_password.txt', user=user, token=token)
    )

def generate_verification_token(user, expires_in=86400):
    """Generate a JWT token for email verification."""
    return jwt.encode(
        {
            'verify_email': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def generate_reset_token(user, expires_in=3600):
    """Generate a JWT token for password reset."""
    return jwt.encode(
        {
            'reset_password': user.id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

def verify_token(token, purpose):
    """Verify a JWT token for either email verification or password reset."""
    try:
        data = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        if purpose in data:
            return User.query.get(data[purpose])
    except:
        return None
    return None 