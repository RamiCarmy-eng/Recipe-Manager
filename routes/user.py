
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash
from models.models import User, Recipe, Favorite, ShoppingList, UserActivity
from extensions import db
from forms.user import UserProfileForm, ChangePasswordForm
from flask_login import login_required, current_user, logout_user
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from datetime import datetime
import os
from werkzeug.utils import secure_filename


user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    recipes_count = Recipe.query.filter_by(user_id=current_user.id).count()
    favorites_count = Favorite.query.filter_by(user_id=current_user.id).count()
    shopping_lists_count = ShoppingList.query.filter_by(user_id=current_user.id).count()
    recent_activity = UserActivity.query.filter_by(user_id=current_user.id).order_by(UserActivity.timestamp.desc()).limit(5).all()

    return render_template(
        'user/profile.html',
        user=current_user,
        recipes_count=recipes_count,
        favorites_count=favorites_count,
        shopping_lists_count=shopping_lists_count,
        recent_activity=recent_activity
    )


@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        try:
            current_user.username = form.username.data
            current_user.email = form.email.data
            
            if form.avatar.data:
                # Handle avatar upload
                filename = secure_filename(form.avatar.data.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', filename)
                form.avatar.data.save(filepath)
                current_user.avatar = f'uploads/avatars/{filename}'
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('user.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
    
    return render_template('user/edit_profile.html', form=form)

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.current_password.data):
            current_user.password = generate_password_hash(form.new_password.data)
            current_user.updated_at = datetime.utcnow()
            
            # Log the password change
            activity = UserActivity(
                user_id=current_user.id,
                action='password_change',
                ip_address=request.remote_addr
            )
            
            db.session.add(activity)
            db.session.commit()
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('user.profile'))
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('user/change_password.html', form=form)

@user_bp.route('/favorites')
@login_required
def favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('user/favorites.html', favorites=favorites)

@user_bp.route('/activity')
@login_required
def activity():
    page = request.args.get('page', 1, type=int)
    activities = UserActivity.query.filter_by(user_id=current_user.id)\
        .order_by(UserActivity.timestamp.desc())\
        .paginate(page=page, per_page=20)
    return render_template('user/activity.html', activities=activities)

@user_bp.route('/api/activity')
@login_required
def get_activity():
    activities = UserActivity.query.filter_by(user_id=current_user.id)\
        .order_by(UserActivity.timestamp.desc())\
        .limit(10)\
        .all()
    
    return jsonify([{
        'action': activity.action,
        'details': activity.details,
        'timestamp': activity.timestamp.isoformat()
    } for activity in activities])

@user_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        try:
            # Update user settings
            current_user.email_notifications = request.form.get('email_notifications') == 'on'
            current_user.public_profile = request.form.get('public_profile') == 'on'
            
            db.session.commit()
            flash('Settings updated successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating settings: {str(e)}', 'error')
    
    return render_template('user/settings.html', user=current_user)

@user_bp.route('/deactivate', methods=['POST'])
@login_required
def deactivate_account():
    try:
        current_user.is_active = False
        current_user.deactivated_at = datetime.utcnow()
        
        # Log the account deactivation
        activity = UserActivity(
            user_id=current_user.id,
            action='account_deactivation',
            ip_address=request.remote_addr
        )
        
        db.session.add(activity)
        db.session.commit()
        
        logout_user()
        flash('Your account has been deactivated.', 'info')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deactivating account: {str(e)}', 'error')
        return redirect(url_for('user.settings')) 