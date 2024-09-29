from flask import Blueprint, request
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

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""
    logging.debug("Register user request received")
    try:
        body_data = request.get_json()
        if not body_data:
            return {"error": "Request must be JSON"}, 400

        user = User(
            name=body_data.get("name"),
            email=body_data.get("email"),
        )

        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully", "user": UserSchema().dump(user)}, 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
        logging.error(f"IntegrityError: {err}")
        return {"error": "Failed to register user."}, 500

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """Get all users (admin only)."""
    current_user = get_jwt_identity()
    # Placeholder for admin check
    if current_user['role'] != 'admin':
        return {"error": "Unauthorized access."}, 403

    try:
        users = User.query.all()
        return UserSchema(many=True).dump(users), 200
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return {"error": "Failed to fetch users."}, 500

@auth_bp.route("/login", methods=["POST"])
def login_user():
    """Authenticate a user and return a JWT."""
    body_data = request.get_json()

    if not body_data or 'email' not in body_data or 'password' not in body_data:
        return {"error": "Email and password are required."}, 400

    try:
        user = User.query.filter_by(email=body_data["email"]).first()
        if user and bcrypt.check_password_hash(user.password, body_data["password"]):
            expires = timedelta(days=1)
            access_token = create_access_token(identity={"email": user.email}, expires_delta=expires)
            return {"access_token": access_token}, 200

        return {"error": "Invalid email or password."}, 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return {"error": "An error occurred during login."}, 500

@auth_bp.route("/", methods=["PATCH"])
@jwt_required()
def update_user():
    """Update the user details."""
    body_data = request.get_json()
    current_user_email = get_jwt_identity()["email"]

    try:
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return {"error": "User not found."}, 404

        if 'name' in body_data:
            user.name = body_data["name"]
        if 'email' in body_data:
            user.email = body_data["email"]
        if 'password' in body_data:
            user.password = bcrypt.generate_password_hash(body_data["password"]).decode("utf-8")

        db.session.commit()
        return UserSchema().dump(user), 200

    except Exception as e:
        logging.error(f"Error updating user profile: {e}")
        db.session.rollback()
        return {"error": "Failed to update user profile."}, 500