from flask_login import UserMixin
from functools import wraps
from flask_login import LoginManager, current_user
from werkzeug.security import check_password_hash
from models import User
from flask import jsonify

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_needed(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error":"Login Required! "}), 401
            if current_user.role != required_role:
                return jsonify({"error":"Unauthorized Acess! "}), 403
            return(f)(*args, **kwargs)
        return wrapper
    return decorator