from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import ShoppingListTemplate, TemplateItem, Ingredient, User
from extensions import db

template_bp = Blueprint('template', __name__)

@template_bp.route('/templates')
@login_required
def list_templates():
    templates = ShoppingListTemplate.query.filter_by(user_id=current_user.id).all()
    return render_template('shopping/templates.html', templates=templates)

@template_bp.route('/template/create', methods=['GET', 'POST'])
@login_required
def create_template():
    if request.method == 'POST':
        template = ShoppingListTemplate(
            name=request.form.get('name'),
            user_id=current_user.id
        )
        db.session.add(template)
        db.session.flush()
        
        # Add items from the form
        items = request.form.getlist('items[]')
        quantities = request.form.getlist('quantities[]')
        units = request.form.getlist('units[]')
        
        for item_id, qty, unit in zip(items, quantities, units):
            template_item = TemplateItem(
                template_id=template.id,
                ingredient_id=item_id,
                quantity=float(qty),
                unit=unit
            )
            db.session.add(template_item)
        
        db.session.commit()
        return redirect(url_for('template.list_templates'))
    
    return render_template('shopping/create_template.html')

@template_bp.route('/templates/<int:template_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_template(template_id):
    template = ShoppingListTemplate.query.get_or_404(template_id)
    
    if template.user_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('template.list_templates'))
    
    if request.method == 'POST':
        # Handle adding/removing items
        pass
        
    return render_template('template/edit.html', template=template)

@template_bp.route('/template/<int:template_id>/use')
@login_required
def use_template(template_id):
    template = ShoppingListTemplate.query.get_or_404(template_id)
    
    # Create new shopping list from template
    shopping_list = ShoppingList(
        name=f"List from {template.name}",
        user_id=current_user.id
    )
    db.session.add(shopping_list)
    db.session.flush()
    
    # Copy items from template
    for template_item in template.items:
        list_item = ShoppingListItem(
            shopping_list_id=shopping_list.id,
            ingredient_id=template_item.ingredient_id,
            quantity=template_item.quantity,
            unit=template_item.unit
        )
        db.session.add(list_item)
    
    db.session.commit()
    return redirect(url_for('shopping.view_shopping_list', list_id=shopping_list.id))

@template_bp.route('/template/<int:template_id>/share', methods=['POST'])
@login_required
def share_template(template_id):
    template = ShoppingListTemplate.query.get_or_404(template_id)
    
    # Ensure user owns the template
    if template.user_id != current_user.id:
        abort(403)
    
    username = request.form.get('username')
    user_to_share_with = User.query.filter_by(username=username).first()
    
    if not user_to_share_with:
        return jsonify({'error': 'User not found'}), 404
    
    # Create new template for the other user
    shared_template = ShoppingListTemplate(
        name=f"{template.name} (Shared by {current_user.username})",
        user_id=user_to_share_with.id,
        shared_from=template.id
    )
    db.session.add(shared_template)
    db.session.flush()
    
    # Copy template items
    for item in template.items:
        shared_item = TemplateItem(
            template_id=shared_template.id,
            ingredient_id=item.ingredient_id,
            quantity=item.quantity,
            unit=item.unit
        )
        db.session.add(shared_item)
    
    db.session.commit()
    return jsonify({'success': True})
