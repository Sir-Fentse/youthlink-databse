from flask import Flask, request, jsonify
from models import db, User
from pathlib import Path
from werkzeug.security import check_password_hash

from routes.students import students_bp
from routes.employers import employers_bp
from routes.users import users_bp
from routes.admin import admin_bp
# from routes.admin import admin_bp   # add this once admin routes are ready

app = Flask(__name__)

# Points to the directory containing this file
BASE_DIR = Path(__file__).resolve().parent
# Explicitly name the DB file
DB_PATH = BASE_DIR / "youthlink-database" / "youthlink.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and check_password_hash(user.password, data["password"]):
        return jsonify({
            "message": "Login successful!",
            "role": user.role
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH.as_posix()}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create the database if not already there
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(students_bp, url_prefix="/api/students")
app.register_blueprint(employers_bp, url_prefix="/api/employers")
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(admin_bp, url_prefix="/api/admins")
if __name__ == "__main__":
    app.run(debug=True)
