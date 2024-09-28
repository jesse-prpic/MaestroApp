from flask_jwt_extended import get_jwt_identity
import functools
from init import db
from models.user import User

def auth_as_admin(fn):
    """Decorator to require admin access.

    Args:
        fn (function): Function to decorate.

    Returns:
        function: Wrapped function with admin check.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()  # Get user ID from JWT
        user = db.session.scalar(db.select(User).filter_by(id=user_id))  # Fetch user
        
        # Check admin status
        if user and user.is_admin:
            return fn(*args, **kwargs)
        return {"error": "Only admin can perform this action"}, 403
    
    return wrapper