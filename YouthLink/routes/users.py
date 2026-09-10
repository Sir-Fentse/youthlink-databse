from flask import Blueprint, request, jsonify
from flask_login import LoginManager
from flask_login import login_required
from models import db, User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from auth import role_needed



users_bp = Blueprint("users", __name__)

@users_bp.route("/register", methods=["POST"])
def create_user():
    data = request.json

    # Hash the password before saving
    hashed_pw = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_pw,   # store hashed password
        role=data["role"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully!",
        "user": {
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }
    }), 201


@users_bp.route("/", methods=["GET"])
@login_required
@role_needed("admin")
def get_all_users():
    users = User.query.all()
    return jsonify([u.username for u in users])


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        return jsonify({
            "message": "Login successful!",
            "role": user.role
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


def get_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "Username": u.username,
            "Email": u.email,
            "Role": u.role
        })
    return jsonify(result), 200
