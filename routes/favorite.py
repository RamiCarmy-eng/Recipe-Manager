from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Favorite, Recipe
from extensions import db

favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/favorites')
@login_required
def list_favorites():
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorite/list.html', favorites=favorites)

@favorite_bp.route('/recipe/<int:recipe_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        recipe_id=recipe_id
    ).first()
    
    if favorite:
        db.session.delete(favorite)
        flash('Recipe removed from favorites')
    else:
        favorite = Favorite(user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(favorite)
        flash('Recipe added to favorites')
    
    db.session.commit()
    return redirect(url_for('recipe.view', recipe_id=recipe_id))
