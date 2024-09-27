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

# setting up and configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# creating a Blueprint for authentication-related routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    logging.debug("register user request received")
    try:
        body_data = request.get_json() # get JSON request Data
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email"),
        )
        if not body_data:
            return {"error": "Request must be JSON"}, 400

        password = body_data.get("password")
        if password:
            # Hash the password before storing
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.add(user) # Add user to the session
        db.session.commit() # Commit the session
        return {f"message": "User registered successfully", "user": UserSchema().dump(user)}, 201
    except IntegrityError as err:
        # Handle database integrity errors
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
            # Not null violation
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
            # unique violation

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    return UserSchema(many=True).dump(users)

@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # Delete a use account (admin only)
    current_user = User.query.get(get_jwt_identity())
    """Delete a user account (admin only)."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}, 204

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    """Logout the user by invalidating the token."""
    # Implementation depends on how you manage token revocation
    return {"message": "User logged out successfully"}, 200

@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Login a user and return a JWT
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt) # Fetch user by email
    
    # Validate user credentials
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # Create JWT token for the user
        token = create_access_token(identity=int(user.id), expires_delta=timedelta(days=7))
        return {"email": user.email, "token": token}
    
    else:
        # Invalid response due to credentials
        return {"error": "Invalid email or password"}, 400