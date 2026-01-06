"""Publisher routes."""
from functools import wraps
from flask import render_template, abort
from flask_login import login_required, current_user

from app.publisher import bp


def role_required(*roles):
    """Decorator to require specific roles. ADMIN always has access."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role != 'ADMIN' and current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@bp.route('/dashboard')
@login_required
@role_required('PUBLISHER', 'ADMIN')
def dashboard():
    """Publisher dashboard."""
    return render_template('publisher/dashboard.html')

