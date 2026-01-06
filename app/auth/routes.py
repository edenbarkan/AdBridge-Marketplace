"""Authentication routes."""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.auth import bp
from app.extensions import db
from app.models import User, PublisherProfile, AdvertiserProfile


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        role = request.form.get('role', '').strip()
        
        # Validation
        if not email or not password or not password_confirm:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')
        
        if password != password_confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('auth/register.html')
        
        if role not in ['PUBLISHER', 'ADVERTISER']:
            flash('Please select a valid role.', 'error')
            return render_template('auth/register.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
        
        # Create user
        try:
            user = User(email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Get user.id
            
            # Create profile based on role
            if role == 'PUBLISHER':
                display_name = request.form.get('display_name', '').strip() or email.split('@')[0]
                domain = request.form.get('domain', '').strip() or None
                profile = PublisherProfile(
                    user_id=user.id,
                    display_name=display_name,
                    domain=domain
                )
            else:  # ADVERTISER
                company_name = request.form.get('company_name', '').strip() or email.split('@')[0]
                profile = AdvertiserProfile(
                    user_id=user.id,
                    company_name=company_name
                )
            
            db.session.add(profile)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('auth/register.html')


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

