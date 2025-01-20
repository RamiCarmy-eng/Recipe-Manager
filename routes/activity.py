from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.models import UserActivity
from datetime import datetime

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/activity')
@login_required
def activity_log():
    activities = UserActivity.query.filter_by(user_id=current_user.id)\
        .order_by(UserActivity.timestamp.desc())\
        .paginate(page=1, per_page=20)
    return render_template('activity/log.html', activities=activities)

@activity_bp.route('/activity/latest')
@login_required
def latest_activities():
    activities = UserActivity.query.filter_by(user_id=current_user.id)\
        .order_by(UserActivity.timestamp.desc())\
        .limit(5)\
        .all()
    
    return jsonify([{
        'action': activity.action,
        'details': activity.details,
        'timestamp': activity.timestamp.isoformat()
    } for activity in activities]) 