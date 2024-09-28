from flask import Blueprint, request, jsonify
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta
from schemas.user_schema import UserSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from utility_functions import auth_as_admin

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""
    logging.debug("Register user request received")
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("name") or not body_data.get("email") or not body_data.get("password"):
            return {"error": "All fields are required"}, 400
        
        user = User(
            name=body_data["name"],
            email=body_data["email"],
            password=bcrypt.generate_password_hash(body_data["password"]).decode("utf-8")
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully", "user": UserSchema().dump(user)}, 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
    except Exception as e:
        logging.error(f"Error in register_user: {str(e)}")
        return jsonify({"error": "An error occurred during registration."}), 500

@auth_bp.route("/users", methods=["GET"])
@auth_as_admin
@jwt_required()
def get_users():
    """Get all users (admin only)."""
    try:
        users = User.query.all()
        return UserSchema(many=True).dump(users), 200
    except Exception as e:
        logging.error(f"Error in get_users: {str(e)}")
        return jsonify({"error": "Failed to fetch users."}), 500

@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@auth_as_admin
@jwt_required()
def delete_user(user_id):
    """Delete a user account (admin only)."""
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 204
    except Exception as e:
        logging.error(f"Error in delete_user: {str(e)}")
        return jsonify({"error": "Failed to delete user."}), 500

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    """Logout the user by invalidating the token."""
    return {"message": "User logged out successfully"}, 200

@auth_bp.route("/login", methods=["POST"])
def login_user():
    """Login a user and return a JWT."""
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("email") or not body_data.get("password"):
            return {"error": "Email and password are required"}, 400
        
        user = User.query.filter_by(email=body_data["email"]).first()

        if user and bcrypt.check_password_hash(user.password, body_data["password"]):
            token = create_access_token(identity=int(user.id), expires_delta=timedelta(days=7))
            return {"email": user.email, "token": token}, 200
        
        return {"error": "Invalid email or password"}, 401
    except Exception as e:
        logging.error(f"Error in login_user: {str(e)}")
        return jsonify({"error": "Failed to log in."}), 500