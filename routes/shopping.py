from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, current_app, send_file, make_response
from flask_login import login_required, current_user
from sqlalchemy import func
from extensions import db
from models.models import (
    ShoppingListTemplate, TemplateItem, CollaborativeList,
    CollaborativeListMember, CollaborativeListItem, Recipe, Ingredient
)
import csv
import io
import json

shopping_bp = Blueprint('shopping', __name__)

# View Routes
@shopping_bp.route('/shopping-lists')
@login_required
def shopping_lists():
    templates = ShoppingListTemplate.query.filter_by(user_id=current_user.id).all()
    collab_lists = CollaborativeList.query.join(
        CollaborativeListMember
    ).filter(
        (CollaborativeList.owner_id == current_user.id) |
        (CollaborativeListMember.user_id == current_user.id)
    ).all()
    
    return render_template(
        'shopping/lists.html',
        templates=templates,
        collab_lists=collab_lists
    )

@shopping_bp.route('/shopping-list/<int:list_id>')
@login_required
def view_list(list_id):
    collab_list = CollaborativeList.query.get_or_404(list_id)
    member = CollaborativeListMember.query.filter_by(
        list_id=list_id, 
        user_id=current_user.id
    ).first()
    
    if not member and collab_list.owner_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    items = CollaborativeListItem.query.filter_by(list_id=list_id).all()
    categories = db.session.query(
        func.distinct(CollaborativeListItem.category)
    ).filter_by(list_id=list_id).all()
    
    return render_template(
        'shopping/view_list.html',
        list=collab_list,
        items=items,
        categories=categories,
        can_edit=member.can_edit if member else True
    )

# Template Management
@shopping_bp.route('/api/templates/<int:template_id>/apply', methods=['POST'])
@login_required
def apply_template(template_id):
    list_id = request.json.get('list_id')
    try:
        template = ShoppingListTemplate.query.get_or_404(template_id)
        if template.user_id != current_user.id:
            return jsonify({'error': 'Not authorized'}), 403
        
        items = TemplateItem.query.filter_by(template_id=template_id).all()
        for item in items:
            list_item = CollaborativeListItem(
                list_id=list_id,
                name=item.name,
                amount=item.amount,
                unit=item.unit,
                category=item.category,
                added_by=current_user.id
            )
            db.session.add(list_item)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Recipe Integration
@shopping_bp.route('/api/lists/<int:list_id>/add-recipe', methods=['POST'])
@login_required
def add_recipe_to_list(list_id):
    recipe_id = request.json.get('recipe_id')
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
        
        for ingredient in ingredients:
            item = CollaborativeListItem(
                list_id=list_id,
                name=ingredient.name,
                amount=ingredient.amount,
                unit=ingredient.unit,
                category=f"From Recipe: {recipe.name}",
                added_by=current_user.id
            )
            db.session.add(item)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# List Sharing and Collaboration
@shopping_bp.route('/api/lists/<int:list_id>/share', methods=['POST'])
@login_required
def share_list(list_id):
    data = request.json
    try:
        collab_list = CollaborativeList.query.get_or_404(list_id)
        if collab_list.owner_id != current_user.id:
            return jsonify({'error': 'Not authorized'}), 403
        
        member = CollaborativeListMember(
            list_id=list_id,
            user_id=data['user_id'],
            can_edit=data.get('can_edit', False)
        )
        db.session.add(member)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# List Organization
@shopping_bp.route('/api/lists/<int:list_id>/categories', methods=['GET'])
@login_required
def get_categories(list_id):
    categories = db.session.query(
        func.distinct(CollaborativeListItem.category)
    ).filter_by(list_id=list_id).all()
    return jsonify({'categories': [c[0] for c in categories if c[0]]})

@shopping_bp.route('/api/lists/<int:list_id>/sort', methods=['PUT'])
@login_required
def sort_items(list_id):
    sort_by = request.args.get('sort', 'category')
    items = CollaborativeListItem.query
    
    if sort_by == 'category':
        items = items.order_by(CollaborativeListItem.category, CollaborativeListItem.name)
    elif sort_by == 'name':
        items = items.order_by(CollaborativeListItem.name)
    elif sort_by == 'added':
        items = items.order_by(CollaborativeListItem.created_at.desc())
    
    items = items.filter_by(list_id=list_id).all()
    return jsonify({
        'items': [{
            'id': item.id,
            'name': item.name,
            'amount': item.amount,
            'unit': item.unit,
            'category': item.category,
            'completed': item.completed
        } for item in items]
    })

# Bulk Operations
@shopping_bp.route('/api/lists/<int:list_id>/bulk-add', methods=['POST'])
@login_required
def bulk_add_items(list_id):
    items = request.json.get('items', [])
    try:
        for item_data in items:
            item = CollaborativeListItem(
                list_id=list_id,
                name=item_data['name'],
                amount=item_data.get('amount'),
                unit=item_data.get('unit'),
                category=item_data.get('category'),
                added_by=current_user.id
            )
            db.session.add(item)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@shopping_bp.route('/api/lists/<int:list_id>/bulk-complete', methods=['PUT'])
@login_required
def bulk_complete_items(list_id):
    item_ids = request.json.get('item_ids', [])
    try:
        CollaborativeListItem.query.filter(
            CollaborativeListItem.id.in_(item_ids)
        ).update({
            'completed': True,
            'completed_by': current_user.id,
            'completed_at': datetime.utcnow()
        }, synchronize_session=False)
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# List Statistics
@shopping_bp.route('/api/lists/<int:list_id>/stats', methods=['GET'])
@login_required
def list_statistics(list_id):
    total_items = CollaborativeListItem.query.filter_by(list_id=list_id).count()
    completed_items = CollaborativeListItem.query.filter_by(
        list_id=list_id, 
        completed=True
    ).count()
    
    categories = db.session.query(
        CollaborativeListItem.category,
        func.count(CollaborativeListItem.id)
    ).filter_by(
        list_id=list_id
    ).group_by(
        CollaborativeListItem.category
    ).all()
    
    return jsonify({
        'total_items': total_items,
        'completed_items': completed_items,
        'completion_rate': (completed_items / total_items * 100) if total_items > 0 else 0,
        'categories': [{
            'name': cat[0] or 'Uncategorized',
            'count': cat[1]
        } for cat in categories]
    })

# Export/Import Features
@shopping_bp.route('/api/lists/<int:list_id>/export', methods=['GET'])
@login_required
def export_list(list_id):
    format_type = request.args.get('format', 'json')
    list_data = CollaborativeList.query.get_or_404(list_id)
    items = CollaborativeListItem.query.filter_by(list_id=list_id).all()
    
    if format_type == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Amount', 'Unit', 'Category', 'Completed'])
        
        for item in items:
            writer.writerow([
                item.name,
                item.amount or '',
                item.unit or '',
                item.category or '',
                'Yes' if item.completed else 'No'
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'shopping_list_{list_id}_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    
    else:  # JSON format
        data = {
            'list_name': list_data.name,
            'created_at': list_data.created_at.isoformat(),
            'items': [{
                'name': item.name,
                'amount': item.amount,
                'unit': item.unit,
                'category': item.category,
                'completed': item.completed,
                'completed_at': item.completed_at.isoformat() if item.completed_at else None
            } for item in items]
        }
        
        return send_file(
            io.BytesIO(json.dumps(data, indent=2).encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'shopping_list_{list_id}_{datetime.now().strftime("%Y%m%d")}.json'
        )

@shopping_bp.route('/api/lists/<int:list_id>/import', methods=['POST'])
@login_required
def import_list(list_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        if file.filename.endswith('.csv'):
            # Handle CSV import
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.DictReader(stream)
            
            for row in csv_reader:
                item = CollaborativeListItem(
                    list_id=list_id,
                    name=row['Name'],
                    amount=float(row['Amount']) if row['Amount'] else None,
                    unit=row['Unit'] or None,
                    category=row['Category'] or None,
                    completed=row['Completed'].lower() == 'yes',
                    added_by=current_user.id
                )
                db.session.add(item)
        
        else:  # Handle JSON import
            data = json.load(file)
            for item_data in data['items']:
                item = CollaborativeListItem(
                    list_id=list_id,
                    name=item_data['name'],
                    amount=item_data.get('amount'),
                    unit=item_data.get('unit'),
                    category=item_data.get('category'),
                    completed=item_data.get('completed', False),
                    added_by=current_user.id
                )
                db.session.add(item)
        
        db.session.commit()
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Template Export/Import
@shopping_bp.route('/api/templates/<int:template_id>/export', methods=['GET'])
@login_required
def export_template(template_id):
    template = ShoppingListTemplate.query.get_or_404(template_id)
    items = TemplateItem.query.filter_by(template_id=template_id).all()
    
    data = {
        'template_name': template.name,
        'created_at': template.created_at.isoformat(),
        'items': [{
            'name': item.name,
            'amount': item.amount,
            'unit': item.unit,
            'category': item.category
        } for item in items]
    }
    
    return send_file(
        io.BytesIO(json.dumps(data, indent=2).encode('utf-8')),
        mimetype='application/json',
        as_attachment=True,
        download_name=f'template_{template_id}_{datetime.now().strftime("%Y%m%d")}.json'
    )

@shopping_bp.route('/api/templates/import', methods=['POST'])
@login_required
def import_template():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        data = json.load(file)
        template = ShoppingListTemplate(
            user_id=current_user.id,
            name=data['template_name']
        )
        db.session.add(template)
        db.session.flush()
        
        for item_data in data['items']:
            item = TemplateItem(
                template_id=template.id,
                name=item_data['name'],
                amount=item_data.get('amount'),
                unit=item_data.get('unit'),
                category=item_data.get('category')
            )
            db.session.add(item)
        
        db.session.commit()
        return jsonify({'success': True, 'template_id': template.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400