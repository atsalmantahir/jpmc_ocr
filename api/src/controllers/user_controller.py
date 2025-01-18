# controllers/user_controller.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from functools import wraps

user_bp = Blueprint('user', __name__)

# Role-Based Access Control (RBAC) Decorator
def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                return jsonify({'message': 'Permission denied'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@user_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({'message': f'Hello, {current_user.username}, your role is {current_user.role}'}), 200

@user_bp.route('/admin', methods=['GET'])
@login_required
@role_required('admin')  # Only admin role can access this route
def admin():
    return jsonify({'message': 'Welcome to the admin area!'}), 200
