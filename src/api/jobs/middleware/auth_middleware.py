from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# Re-export jwt_required for convenience
jwt_required = jwt_required

def provider_required(f):
    """Decorator to require provider role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_email = get_jwt_identity()
        # Here you would check if the user has provider role
        # For now, we'll assume all authenticated users can access
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    """Decorator to require customer role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_email = get_jwt_identity()
        # Here you would check if the user has customer role
        # For now, we'll assume all authenticated users can access
        return f(*args, **kwargs)
    return decorated_function
