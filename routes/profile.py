from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.models import Recipe, Favorite, UserActivity
from extensions import db
from forms.user import UserProfileForm
import os

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def view_profile():
    recipes = Recipe.query.filter_by(user_id=current_user.id).limit(5).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).limit(5).all()
    activities = UserActivity.query.filter_by(user_id=current_user.id)\
        .order_by(UserActivity.timestamp.desc())\
        .limit(5)\
        .all()
    
    return render_template('profile/view.html',
                         user=current_user,
                         recipes=recipes,
                         favorites=favorites,
                         activities=activities)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        if form.avatar.data:
            file = form.avatar.data
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'avatars', filename)
            file.save(filepath)
            current_user.avatar = f'uploads/avatars/{filename}'
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
    
    return render_template('profile/edit.html', form=form) 