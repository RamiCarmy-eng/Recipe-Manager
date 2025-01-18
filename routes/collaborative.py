from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import CollaborativeList, CollaborativeListMember, CollaborativeListItem
from extensions import db

collaborative_bp = Blueprint('collaborative', __name__)

@collaborative_bp.route('/collaborative/lists')
@login_required
def lists():
    user_lists = CollaborativeList.query.filter_by(owner_id=current_user.id).all()
    shared_lists = CollaborativeListMember.query.filter_by(user_id=current_user.id).all()
    return render_template('collaborative/lists.html', 
                         user_lists=user_lists, 
                         shared_lists=shared_lists)

@collaborative_bp.route('/collaborative/create', methods=['GET', 'POST'])
@login_required
def create_list():
    if request.method == 'POST':
        name = request.form.get('name')
        new_list = CollaborativeList(name=name, owner_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('collaborative.lists'))
    return render_template('collaborative/create.html')

@collaborative_bp.route('/collaborative/<int:list_id>/add_member', methods=['POST'])
@login_required
def add_member(list_id):
    collab_list = CollaborativeList.query.get_or_404(list_id)
    if collab_list.owner_id != current_user.id:
        flash('Not authorized')
        return redirect(url_for('collaborative.lists'))
    
    user_email = request.form.get('email')
    can_edit = request.form.get('can_edit') == 'true'
    # Add member logic here
    return redirect(url_for('collaborative.lists'))
