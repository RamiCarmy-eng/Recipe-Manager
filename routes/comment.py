from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Comment, Recipe
from extensions import db

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/recipe/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    content = request.form.get('content')
    
    if content:
        comment = Comment(
            user_id=current_user.id,
            recipe_id=recipe_id,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully')
    
    return redirect(url_for('recipe.view', recipe_id=recipe_id))

@comment_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id == current_user.id:
        recipe_id = comment.recipe_id
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully')
        return redirect(url_for('recipe.view', recipe_id=recipe_id))
    
    flash('Not authorized to delete this comment')
    return redirect(url_for('recipe.view', recipe_id=comment.recipe_id))
