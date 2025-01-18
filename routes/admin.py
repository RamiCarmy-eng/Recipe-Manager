from flask import (
    Blueprint, jsonify, redirect, url_for, flash, 
    session, current_app, render_template
)
from flask_login import login_required, current_user
from models import User, Recipe, Comment, Favorite
from extensions import db
from decorators import admin_required
import os

admin_bp = Blueprint('admin', __name__)

def delete_image(filename):
    """Helper function to delete image files"""
    if not filename:
        return
    
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting image {filename}: {e}")

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    recipes = Recipe.query.all()
    return render_template('admin/dashboard.html', users=users, recipes=recipes)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/recipes_images')
@login_required
@admin_required
def recipes():
    recipes = Recipe.query.all()
    return render_template('admin/recipes_images.html', recipes=recipes)

@admin_bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'User {user.username} {"activated" if user.is_active else "deactivated"}', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/recipe/<int:recipe_id>/toggle-featured', methods=['POST'])
@login_required
@admin_required
def toggle_recipe_featured(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.is_featured = not recipe.is_featured
    db.session.commit()
    flash(f'Recipe {recipe.name} {"featured" if recipe.is_featured else "unfeatured"}', 'success')
    return redirect(url_for('admin.recipes_images'))

@admin_bp.route('/recipe/<int:recipe_id>/toggle-hidden', methods=['POST'])
@login_required
@admin_required
def toggle_recipe_hidden(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.is_hidden = not recipe.is_hidden
    db.session.commit()
    flash(f'Recipe {recipe.name} {"hidden" if recipe.is_hidden else "unhidden"}', 'success')
    return redirect(url_for('admin.recipes_images'))

# API route for AJAX calls
@admin_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def api_delete_user(user_id):
    try:
        user = db.session.query(User).get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'})

        # Prevent self-deletion
        if user.id == current_user.id:
            return jsonify({
                'success': False,
                'message': 'Cannot delete your own account'
            })

        # Delete user's recipes_images, comments, and favorites
        db.session.query(Favorite).filter_by(user_id=user_id).delete()
        db.session.query(Comment).filter_by(user_id=user_id).delete()

        # Get recipes_images to delete their images
        recipes = db.session.query(Recipe).filter_by(user_id=user_id).all()
        for recipe in recipes:
            if recipe.image:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], recipe.image))
                except:
                    pass  # Image might not exist

        db.session.query(Recipe).filter_by(user_id=user_id).delete()

        # Finally delete the user
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User and all associated data deleted'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

# Web route for form submissions
@admin_bp.route('/user/<int:id>/delete', methods=['POST'])
@admin_required
def web_delete_user(id):
    if id == session.get('user_id'):
        flash('Cannot delete your own account.')
        return redirect(url_for('admin.manage_users'))

    user = User.query.get_or_404(id)

    try:
        # Delete user's avatar if exists
        if user.avatar:
            delete_image(user.avatar)

        # Delete user's recipe images
        for recipe in user.recipes:
            if recipe.image:
                delete_image(recipe.image)

        # Delete user and all associated data (SQLAlchemy will handle relationships)
        db.session.delete(user)
        db.session.commit()

        flash('User and all associated data deleted successfully.')

    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {e}')

    return redirect(url_for('admin.manage_users')) 