from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import ShoppingListTemplate, TemplateItem
from extensions import db

template_bp = Blueprint('template', __name__)

@template_bp.route('/templates')
@login_required
def list_templates():
    templates = ShoppingListTemplate.query.filter_by(user_id=current_user.id).all()
    return render_template('template/list.html', templates=templates)

@template_bp.route('/templates/create', methods=['GET', 'POST'])
@login_required
def create_template():
    if request.method == 'POST':
        name = request.form.get('name')
        template = ShoppingListTemplate(
            user_id=current_user.id,
            name=name
        )
        db.session.add(template)
        db.session.commit()
        return redirect(url_for('template.edit_template', template_id=template.id))
    
    return render_template('template/create.html')

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

@template_bp.route('/templates/<int:template_id>/use', methods=['POST'])
@login_required
def use_template(template_id):
    template = ShoppingListTemplate.query.get_or_404(template_id)
    
    if template.user_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('template.list_templates'))
    
    # Create new shopping list from template
    # Add logic here
    
    return redirect(url_for('shopping.view_list', list_id=new_list.id))
