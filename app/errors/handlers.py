"""Error handlers."""
from flask import render_template

from app.errors import bp


@bp.app_errorhandler(403)
def forbidden_error(error):
    """403 Forbidden error handler."""
    return render_template('errors/403.html'), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    """404 Not Found error handler."""
    return render_template('errors/404.html'), 404

