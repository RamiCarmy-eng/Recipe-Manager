from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.models import  UserActivity
from extensions import db

from wtforms import  EmailField
from wtforms.validators import ValidationError
from models.models import User
from forms.auth import LoginForm
from datetime import datetime
auth_bp = Blueprint('auth', __name__)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import login_user, logout_user, login_required, current_user

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.recipes'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('auth/register.html', form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html', form=form)

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            created_at=datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.recipes'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            # Login the user first
            login_user(user, remember=form.remember_me.data)

            # Log the login activity
            activity = UserActivity(
                user_id=user.id,
                action='login',
                ip_address=request.remote_addr,
                timestamp=datetime.utcnow()
            )
            db.session.add(activity)

            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Get next page from request args (only get it once)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.recipes'))

        flash('Invalid username or password', 'error')

    return render_template('auth/login.html', form=form, title='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    # Log the logout activity
    activity = UserActivity(
        user_id=current_user.id,
        action='logout',
        ip_address=request.remote_addr,
        timestamp=datetime.utcnow()
    )
    db.session.add(activity)
    db.session.commit()

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        if email and email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('Email already exists', 'error')
            else:
                current_user.email = email
        
        if current_password and new_password:
            if check_password_hash(current_user.password_hash, current_password):
                current_user.password_hash = generate_password_hash(new_password)
                flash('Password updated successfully', 'success')
            else:
                flash('Current password is incorrect', 'error')
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html')

# Add admin user creation route (temporary, remove in production)
@auth_bp.route('/create-admin')
def create_admin():
    # Check if admin already exists
    admin = User.query.filter_by(username='admin').first()
    if admin:
        flash('Admin user already exists!')
        return redirect(url_for('auth.login'))
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password=generate_password_hash('admin123'),  # Change this password!
        role='admin'
    )
    
    try:
        db.session.add(admin)
        db.session.commit()
        flash('Admin user created successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating admin: {str(e)}')
    
    return redirect(url_for('auth.login'))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=4, max=80, message="Username must be between 4 and 80 characters")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=4, max=80, message="Username must be between 4 and 80 characters")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address"),
        Length(max=120, message="Email must be less than 120 characters")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
