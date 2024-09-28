from flask_jwt_extended import get_jwt_identity
import functools
from init import db
from models.user import User

def auth_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the user's ID from JWT identity
        user_id = get_jwt_identity()
        
        # Fetch the user from the database
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        
        # Check if the user is an admin
        if user and user.is_admin:  # Ensure user exists and is admin
            return fn(*args, **kwargs)
        else:
            return {"error": "Only admin can perform this action"}, 403
    
    return wrapper