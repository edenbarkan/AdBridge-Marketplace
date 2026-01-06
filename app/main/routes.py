"""Main routes."""
from flask import render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user

from app.main import bp


@bp.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard redirect based on role."""
    role = current_user.role
    
    if role == 'PUBLISHER':
        return redirect(url_for('publisher.dashboard'))
    elif role == 'ADVERTISER':
        return redirect(url_for('advertiser.dashboard'))
    elif role == 'ADMIN':
        return redirect(url_for('admin.dashboard'))
    else:
        return redirect(url_for('main.index'))


@bp.route('/healthz')
def healthz():
    """Health check endpoint for K8s."""
    return jsonify({'status': 'ok'}), 200

