from flask import Blueprint, request
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta
from schemas.user_schema import UserSchema
from models.user import User
import logging

# setting up and configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# from flask_jwt_extended import jwt_required, create_refresh_token

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
    
# @auth_bp.route("/token/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh_token():
#     current_user = get_jwt_identity()
#     new_token = create_access_token(identity=current_user)
#     return {"access_token": new_token}, 200