from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


class AuthConfig:
    # Authentication settings
    LOGIN_DISABLED = False
    SESSION_PROTECTION = 'strong'
    REMEMBER_COOKIE_DURATION = 30  # days
    REMEMBER_COOKIE_SECURE = False  # Set to True in production
    REMEMBER_COOKIE_HTTPONLY = True