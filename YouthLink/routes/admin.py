from flask import Blueprint, request, jsonify
from models import db, Admin

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/", methods=["POST"])
def create_admin():
    data = request.get_json()

    new_admin = Admin(
        name=data["name"],
        id_key=data["id_key"]
    )
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({
        "message": "Admin registered successfully!",
        "admin": {
            "Name": new_admin.name,
            "Id_Key": new_admin.id_key
        }
    }), 201

@admin_bp.route("/", methods=["GET"])
def get_admin():
    admins = Admin.query.all()
    result = []
    for a in admins:
        result.append({
            "Name": a.name,
            "Id_Key": a.id_key
        })
    return jsonify(result), 200

@admin_bp.route("/<int:id>", methods=["PUT"])
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        admin.name = data["name"]
    if "id_key" in data:
        admin.id_key = data["id_key"]

    db.session.commit()
    return jsonify({
        "message": "Admin updated successfully!",
        "admin": {
            "Name": admin.name,
            "Id_Key": admin.id_key
        }
    }), 200
