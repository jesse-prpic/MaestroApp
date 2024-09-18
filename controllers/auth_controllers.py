from flask import Blueprint, request
from models import User, UserSchema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    body_data = request.get_json()
    user = User(
        name=body_data.get("name"),
        email=body_data.get("email"),
    )
    password = body_data.get("password")
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    try:
        db.session.add(user)
        db.session.commit()
        return UserSchema().dump(user), 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email must be unique"}, 400

@auth_bp.route("/login", methods=["POST"])
def login_user():
    body_data = request.get_json()
    stmt = select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {"email": user.email, "token": token}
    
    return {"error": "Invalid email or password"}, 400