from flask import Blueprint

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/list')
def list_notifications():
    return "Notifications list" 