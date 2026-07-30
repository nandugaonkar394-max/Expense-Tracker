from flask import Blueprint, request, jsonify
from models import db, User

api = Blueprint("api", __name__)


@api.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User Registered Successfully"})


@api.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({

    "message":"Login successful",

    "user_id":user.id

})
    return jsonify({"message": "Invalid Email or Password"}), 401

