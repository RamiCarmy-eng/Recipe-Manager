from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.models import User, UserPreference
from extensions import db

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings')
@login_required
def user_settings():
    preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
    return render_template('settings/preferences.html', preferences=preferences)

@settings_bp.route('/settings/update', methods=['POST'])
@login_required
def update_settings():
    try:
        preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
        if not preferences:
            preferences = UserPreference(user_id=current_user.id)
            db.session.add(preferences)
        
        preferences.email_notifications = request.form.get('email_notifications') == 'on'
        preferences.public_profile = request.form.get('public_profile') == 'on'
        preferences.default_servings = int(request.form.get('default_servings', 4))
        preferences.measurement_system = request.form.get('measurement_system', 'metric')
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating settings: {str(e)}', 'error')
    
    return redirect(url_for('settings.user_settings'))

@settings_bp.route('/settings/notifications')
@login_required
def notification_settings():
    return render_template('settings/notifications.html')

@settings_bp.route('/settings/privacy')
@login_required
def privacy_settings():
    return render_template('settings/privacy.html') 