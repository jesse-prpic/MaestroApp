from flask import Blueprint, request
from init import bcrypt, db, ma
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta
from schemas.user_schema import UserSchema
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        body_data = request.get_json()
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email"),
        )
        if not body_data:
            return {"error": "Request must be JSON"}, 400

        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.add(user)
        db.session.commit()
        return {f"message": "User registered successfully", "user": UserSchema().dump(user)}, 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 400
            # Not null violation
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address must be unique"}, 400
            # unique violation

@auth_bp.route("/login", methods=["POST"])
def login_user():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=int(user.id), expires_delta=timedelta(days=7))
        return {"email": user.email, "token": token}
    
    else:
        return {"error": "Invalid email or password"}, 400