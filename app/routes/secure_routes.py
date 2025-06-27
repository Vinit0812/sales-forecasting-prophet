from flask import Blueprint, jsonify
from app.utils.jwt_utils import token_required

secure_bp = Blueprint("secure_bp", __name__)

@secure_bp.route("/secure-data", methods=["GET"])
@token_required
def secure_data():
    return jsonify({"message": "🔐 Access granted to secure data!"})
