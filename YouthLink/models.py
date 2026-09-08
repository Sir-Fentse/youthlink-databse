from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # store hashed password
    email = db.Column(db.String(200), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    id_key = db.Column(db.Integer, unique=True, nullable=False)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    school_name = db.Column(db.String(200), nullable=False)
    interests = db.Column(db.String(200), nullable=False)
    qualifications = db.Column(db.String(200), nullable=False)
    applications = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="student", uselist=False)

class Employer(db.Model):
    __tablename__ = "employers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    industry = db.Column(db.String(200), nullable=False)
    opportunities = db.Column(db.String(200), nullable=True)
    company_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="employer", uselist=False)
