from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///youthlink.db'
db = SQLAlchemy(app)

#defining a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    skills = db.Column(db.String(200))
    interests = db.Column(db.String(200))

#create database file
with app.app_context():
    db.create_all() #this builds a table in the database file where User information will be stored


@app.route("/") #similar to an if statement, if someone gets to this point then...
def home():
    return("Welcome to Youth-Link")

@app.route("/about")
def about():
    return("Youth Link is about connecting aspiring students to career defining opportunities!")

@app.route("/api/Users", methods = ["POST"])
def create_User():
    data = request.json
    new_User = User(
        name = data["name"],
        age = data["age"],
        skills = ",".join(data.get("skills", [])),
        interests = ",".join(data.get("interests", []))

    )
    db.session.add(new_User)
    db.session.commit()
    return jsonify({
        "message":"User Created!",
        "User": data
        }), 201


@app.route("/api/Users", methods = ["GET"])
def get_Users():
    Users = User.query.all()
    result = []
    for u in Users:
        result.append({
            "id": u.id,
            "name": u.name,
            "age": u.age,
            "skills": u.skills.split(",")
            if u.skills else[],
            "interests":u.interests.split(",") if u.interests else[]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)