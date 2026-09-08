from flask import Blueprint, request, jsonify
from models import db, Student, User
from werkzeug.security import generate_password_hash

students_bp = Blueprint("students", __name__)

@students_bp.route("/", methods=["POST"])
def create_student():
    data = request.get_json()

    # Create linked User record with hashed password
    hashed_pw = generate_password_hash(data["password"])
    new_user = User(
        username=data["name"],
        email=data["email"],
        password=hashed_pw,
        role="student"
    )
    db.session.add(new_user)
    db.session.commit()

    # Create Student record linked to User
    new_student = Student(
        name=data["name"],
        email=data["email"],
        age=data["age"],
        school_name=data["school_name"],
        qualifications=data["qualifications"],
        interests=data["interests"],
        applications=data.get("applications"),
        user_id=new_user.id
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully!",
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "school_name": new_student.school_name,
            "qualifications": new_student.qualifications,
            "interests": new_student.interests,
            "applications": new_student.applications
        }
    }), 201

@students_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        student.name = data["name"]
    if "email" in data:
        student.email = data["email"]
    if "age" in data:
        student.age = data["age"]
    if "school_name" in data:
        student.school_name = data["school_name"]
    if "qualifications" in data:
        student.qualifications = data["qualifications"]
    if "interests" in data:
        student.interests = data["interests"]
    if "applications" in data:
        student.applications = data["applications"]

    db.session.commit()
    return jsonify({
        "message": "Student updated successfully!",
        "student": {
            "id": student.id,
            "name": student.name,
            "school_name": student.school_name,
            "qualifications": student.qualifications,
            "interests": student.interests,
            "applications": student.applications
        }
    }), 200

@students_bp.route("/", methods=["GET"])
def get_students():
    students = Student.query.all()
    result = []
    for i in students:
        result.append({
            "ID": i.id,
            "Age": i.age,
            "Name": i.name,
            "School": i.school_name,
            "Qualification": i.qualifications,
            "Interests": i.interests,
            "Applications": i.applications
        })
    return jsonify(result), 200
