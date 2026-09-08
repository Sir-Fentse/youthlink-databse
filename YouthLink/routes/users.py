from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["POST"])
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
