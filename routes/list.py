from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import ShoppingList, ShoppingListItem, Recipe
from extensions import db
from datetime import datetime

list_bp = Blueprint('list', __name__)

@list_bp.route('/lists')
@login_required
def my_lists():
    shopping_lists = ShoppingList.query.filter_by(user_id=current_user.id)\
        .order_by(ShoppingList.created_at.desc())\
        .all()
    return render_template('lists/my_lists.html', lists=shopping_lists)

@list_bp.route('/list/create', methods=['GET', 'POST'])
@login_required
def create_list():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            shopping_list = ShoppingList(
                name=name,
                user_id=current_user.id,
                created_at=datetime.utcnow()
            )
            db.session.add(shopping_list)
            db.session.commit()
            flash('Shopping list created successfully!', 'success')
            return redirect(url_for('list.view_list', list_id=shopping_list.id))
    
    return render_template('lists/create.html')

@list_bp.route('/list/<int:list_id>')
@login_required
def view_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        flash('You do not have permission to view this list.', 'danger')
        return redirect(url_for('list.my_lists'))
    
    items = ShoppingListItem.query.filter_by(shopping_list_id=list_id)\
        .order_by(ShoppingListItem.checked, ShoppingListItem.name)\
        .all()
    
    return render_template('lists/view.html',
                         shopping_list=shopping_list,
                         items=items) 