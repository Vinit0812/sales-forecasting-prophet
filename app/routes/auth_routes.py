from flask import Blueprint, request, jsonify
from app.utils.jwt_utils import generate_token

auth_bp = Blueprint("auth_bp", __name__)

# Dummy credentials
USER = {"username": "admin", "password": "admin123"}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Username and password required"}), 400

    if data["username"] == USER["username"] and data["password"] == USER["password"]:
        token = generate_token(data["username"])
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
