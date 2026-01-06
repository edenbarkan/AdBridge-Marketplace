"""Admin routes."""
from functools import wraps
from flask import render_template, abort
from flask_login import login_required, current_user

from app.admin import bp


def role_required(*roles):
    """Decorator to require specific roles."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/dashboard')
@login_required
@role_required('ADMIN')
def dashboard():
    """Admin dashboard."""
    return render_template('admin/dashboard.html')

