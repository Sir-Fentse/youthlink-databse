from flask import Blueprint, request, jsonify
from models import db, Employer, User
from werkzeug.security import generate_password_hash

employers_bp = Blueprint("employers", __name__)

@employers_bp.route("/", methods=["POST"])
def create_employer():
    data = request.get_json()

    # Create linked User record with hashed password
    hashed_pw = generate_password_hash(data["password"])
    new_user = User(
        username=data["name"],
        email=data["email"],
        password=hashed_pw,
        role="employer"
    )
    db.session.add(new_user)
    db.session.commit()

    # Create Employer record linked to User
    new_employer = Employer(
        age=data["age"],
        name=data["name"],
        email=data["email"],
        company_name=data["company_name"],
        industry=data.get("industry"),
        opportunities=data.get("opportunities"),
        user_id=new_user.id
    )
    db.session.add(new_employer)
    db.session.commit()

    return jsonify({
        "message": "Employer registered successfully!",
        "employer": {
            "id": new_employer.id,
            "name": new_employer.name,
            "email": new_employer.email,
            "company_name": new_employer.company_name,
            "industry": new_employer.industry,
            "opportunities": new_employer.opportunities
        }
    }), 201

@employers_bp.route("/", methods=["GET"])
def get_employers():
    employers = Employer.query.all()
    result = []
    for e in employers:
        result.append({
            "ID": e.id,
            "Name": e.name,
            "Email": e.email,
            "Age": e.age,
            "Company_name": e.company_name,
            "Industry": e.industry,
            "Opportunities": e.opportunities
        })
    return jsonify(result), 200

@employers_bp.route("/<int:id>", methods=["PUT"])
def update_employer(id):
    employer = Employer.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        employer.name = data["name"]
    if "age" in data:
        employer.age = data["age"]
    if "email" in data:
        employer.email = data["email"]
    if "company_name" in data:
        employer.company_name = data["company_name"]
    if "industry" in data:
        employer.industry = data["industry"]
    if "opportunities" in data:
        employer.opportunities = data["opportunities"]

    db.session.commit()
    return jsonify({
        "message": "Employer updated successfully!",
        "employer": {
            "id": employer.id,
            "name": employer.name,
            "age": employer.age,
            "company_name": employer.company_name,
            "industry": employer.industry,
            "opportunities": employer.opportunities
        }
    }), 200
